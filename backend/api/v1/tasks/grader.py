#!/usr/bin/env python3
"""Background grader task for processing submissions.

This module is intended to be run by an RQ worker. The `process_submission`
function receives identifiers and runs the tests, saving TestResult objects
and updating the Submission status.
"""
import os
import shutil
import subprocess
import tempfile
from datetime import datetime

from models import storage
from models.test_case import TestCase
from models.test_result import TestResult
from models.submission import Submission
from models.project import Project
from models.task import Task


def _safe_run(cmd, cwd=None, input_data=None, timeout=5):
    """Run subprocess safely and return CompletedProcess or raise."""
    return subprocess.run(cmd, capture_output=True, text=True, input=input_data, timeout=timeout, cwd=cwd)


def process_submission(submission_id, task_id, project_id, user_id, language, file_url):
    """Process a submission: run test cases and save TestResult entries.

    Args:
        submission_id (str)
        task_id (str)
        project_id (str)
        user_id (str)
        language (str)
        file_url (str): path to the submitted file
    """
    submission = storage.get(Submission, submission_id)
    if not submission:
        # Nothing to do
        return {'error': 'submission not found'}

    # gather test cases for task
    test_cases = storage.all(TestCase).values()
    test_case_list = [test_case.to_dict() for test_case in test_cases if test_case.task_id == task_id]

    results = []
    tmpdir = tempfile.mkdtemp(prefix=f"grader_{user_id}_")

    try:
        # Ensure submission file exists
        if not os.path.exists(file_url):
            return {'error': "submitted file missing"}

        # compile/run per language
        def _run_in_docker(image, cmd, workdir, timeout_sec):
            docker_cmd = [
                'docker', 'run', '--rm',
                '--net', 'none',
                '--pids-limit', '64',
                '--cpus', '0.5',
                '--memory', '128m',
                '--read-only',
                '-v', f"{workdir}:/work:rw",
                '--user', '1000:1000',
                '--cap-drop', 'ALL',
                image,
                'sh', '-c', cmd
            ]
            return subprocess.run(docker_cmd, capture_output=True, text=True, timeout=timeout_sec)

        for test_case in test_case_list:
            try:
                code_result = None
                test_result = None

                input_data = test_case.get('input', '')
                if language == 'Python':
                    # Prefer running inside Docker sandbox; fallback to local if docker not available
                    try:
                        cmd = f"python3 /work/{os.path.basename(file_url)}"
                        code_result = _run_in_docker('devarena/python-runner:latest', cmd, tmpdir, 8)
                    except FileNotFoundError:
                        # docker cli not present; run locally
                        code_result = _safe_run(["python3", file_url], input_data=input_data, timeout=5)
                    # For python, the expected output may be stored in test_case['expected']
                    # If test case stores an expected output, compare to student stdout
                    expected = test_case.get('expected')
                    if expected is not None:
                        if code_result.stdout.strip() == expected.strip():
                            results.append({
                                'submission_id': submission_id,
                                'test_case_id': test_case['id'],
                                'name': test_case.get('name'),
                                'status': 'passed',
                                'passed': True
                            })
                        else:
                            results.append({
                                'submission_id': submission_id,
                                'test_case_id': test_case['id'],
                                'name': test_case.get('name'),
                                'status': 'failed',
                                'passed': False,
                                'actual_output': code_result.stdout
                            })
                    else:
                        # No expected field; store stdout as result
                        results.append({
                            'submission_id': submission_id,
                            'test_case_id': test_case['id'],
                            'name': test_case.get('name'),
                            'status': 'passed',
                            'passed': True,
                            'actual_output': code_result.stdout
                        })

                elif language == 'C':
                    # compile and run inside Docker gcc image
                    try:
                        # copy file into tmpdir (worker already has file_url on host)
                        host_submission = file_url
                        host_dest = os.path.join(tmpdir, os.path.basename(file_url))
                        shutil.copy(host_submission, host_dest)
                        # compile inside container
                        compile_cmd = f"gcc /work/{os.path.basename(host_dest)} -o /work/{submission_id}"
                        compiled = _run_in_docker('devarena/c-runner:latest', compile_cmd, tmpdir, 12)
                        if compiled.returncode != 0:
                            results.append({
                                'submission_id': submission_id,
                                'test_case_id': test_case['id'],
                                'name': test_case.get('name'),
                                'status': 'failed',
                                'passed': False,
                                'actual_output': compiled.stderr
                            })
                            continue
                        run_cmd = f"/work/{submission_id}"
                        code_result = _run_in_docker('devarena/c-runner:latest', run_cmd, tmpdir, 6)
                    except FileNotFoundError:
                        # fallback to local compile/run
                        exe_path = os.path.join(tmpdir, f"{submission_id}")
                        compiled = _safe_run(["gcc", file_url, "-o", exe_path], timeout=10)
                        if compiled.returncode != 0:
                            results.append({
                                'submission_id': submission_id,
                                'test_case_id': test_case['id'],
                                'name': test_case.get('name'),
                                'status': 'failed',
                                'passed': False,
                                'actual_output': compiled.stderr
                            })
                            continue
                        code_result = _safe_run([exe_path], input_data=input_data, timeout=5)
                    expected = test_case.get('expected')
                    if expected is not None and code_result.stdout.strip() == expected.strip():
                        results.append({
                            'submission_id': submission_id,
                            'test_case_id': test_case['id'],
                            'name': test_case.get('name'),
                            'status': 'passed',
                            'passed': True
                        })
                    else:
                        results.append({
                            'submission_id': submission_id,
                            'test_case_id': test_case['id'],
                            'name': test_case.get('name'),
                            'status': 'failed',
                            'passed': False,
                            'actual_output': code_result.stdout if code_result else compiled.stderr
                        })

                else:
                    # Unsupported language for now; mark as failed
                    results.append({
                        'submission_id': submission_id,
                        'test_case_id': test_case['id'],
                        'name': test_case.get('name'),
                        'status': 'failed',
                        'passed': False,
                        'actual_output': 'unsupported language'
                    })

            except subprocess.TimeoutExpired:
                results.append({
                    'submission_id': submission_id,
                    'test_case_id': test_case['id'],
                    'name': test_case.get('name'),
                    'status': 'failed',
                    'passed': False,
                    'actual_output': 'timeout'
                })
            except Exception as e:
                results.append({
                    'submission_id': submission_id,
                    'test_case_id': test_case['id'],
                    'name': test_case.get('name'),
                    'status': 'failed',
                    'passed': False,
                    'actual_output': str(e)
                })

        # persist results
        failed = False
        for res in results:
            if res.get('status') == 'failed':
                failed = True
            new_tr = TestResult(**res)
            new_tr.save()

        if failed:
            setattr(submission, 'status', 'failed')
        else:
            setattr(submission, 'status', 'passed')

        storage.save()
        return {'status': 'done', 'results': len(results)}

    finally:
        # cleanup temporary directory
        try:
            shutil.rmtree(tmpdir)
        except Exception:
            pass
