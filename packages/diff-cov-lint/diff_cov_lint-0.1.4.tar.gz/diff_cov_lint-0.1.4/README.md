# Diff cov lint

Linting and coverage reports for git diff only.

## Usage: 

```diff-cov-lint master new_branch --cov_report=coverage.xml --lint_report=pylint_output.txt```

Example output (the command above was run in `tests/repo` folder):
```
======================== DIFF COVERAGE ========================
FILE                                    COVERED STMTS   PERCENT
src/add.py                                    5     8     62.5%
src/modify.py                                 1     2     50.0%
===============================================================
TOTAL DIFF COV                                6    10     60.0%

========================== DIFF LINT ==========================
src/add.py:10:0 E0602: Undefined variable 'this_line_makes_no_sense' (undefined-variable)
```

Arguments:  

POSITIONAL ARGUMENTS  
    `TARGET_REF`
        Target branch in repo  
    `SOURCE_REF`
        Source branch in repo  

FLAGS  
    `--cov_report=COV_REPORT`  
        Path to coverage report in Cobertura (pytest-cov) format, If not stated, coverage report will not be produced.  
    `--lint_report=LINT_REPORT`  
        Path to pylint report. If not stated, linting report will not be produced.  
    `--repo_path=REPO_PATH`  
        Path to repo folder, defaults to "."
    `--show_missing`
        Flag to show missing lines, defaults to false

## CI Setup

This project's repo uses diff-cov-lint itself. You might want to check [.gitlab-ci.yml](https://gitlab.com/sVerentsov/diff-cov-lint/blob/master/.gitlab-ci.yml) for full configuration.

### Simple scenario  
Calculate diff coverage and produce diff pylint reports for merge requests 

```yaml
code_quality_diff: 
    stage: code_quality_diff
    script:
        - pytest --cov=your_source_folder --cov-report xml tests # run pytest and produce xml report
        - git fetch -a # fetch all branches to calculate diff
        - pip install diff-cov-lint # install diff-cov-lint
        - pylint --exit-zero diff_cov_lint > pylint_output.txt # get pylint report. --exit-zero needed for job not to fail if pylint give score less than 10.
        - diff-cov-lint origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME origin/$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME --cov_report coverage.xml --lint_report pylint_output.txt # run diff-cov-lint on diff between target branch and source branch.
    only:
        - merge_requests # required to know target branch and source branch
```

### More complicated scenario  
 - Run tests on each push (test job)
 - Calculate diff coverage and produce diff pylint reports for merge requests (code_quality_diff job)
 - Get coverage and pylint report on full code on master or manually on any push. (code_quality_full job)

Test job: 
```yaml
test: 
    stage: test
    script: 
        - pytest --cov=your_source_folder --cov-report xml tests # run pytest and produce xml report
    artifacts:
        paths: 
            - coverage.xml # save xml report to use it in further jobs
    only:
        - tags  # tags and branches are default values of "only", so preserve them
        - branches
        - merge_requests # add merge_requests since code_quality_diff job will use artifacts of this job
```

Diff code quality job:

```yaml
code_quality_diff: 
    stage: code_quality_diff
    script:
        - git fetch -a # fetch all branches to calculate diff
        - pip install diff-cov-lint # install diff-cov-lint
        - pylint --exit-zero diff_cov_lint > pylint_output.txt # get pylint report. --exit-zero needed for job not to fail if pylint give score less than 10.
        - diff-cov-lint origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME origin/$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME --cov_report coverage.xml --lint_report pylint_output.txt # run diff-cov-lint on diff between target branch and source branch. coverage.xml is used from the artifact.
    only:
        - merge_requests
```

Full code quality job:

```yaml
code_quality_full:
    stage:
        code_quality_full
    script:
        - pytest --cov=your_source_folder tests # simply run pytest with coverage and pylint as usual
        - pylint --exit-zero diff_cov_lint
    rules:
        - if: '$CI_COMMIT_REF_NAME == "master"'
        - if: $CI_MERGE_REQUEST_ID
          when: never #otherwise this job will stuck for merge requests
        - when: manual # use manual to make this job optional for all other pipelines. 
```