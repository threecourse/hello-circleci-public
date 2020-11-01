curl -u ${CIRCLE_API_USER_TOKEN}: \
     -d build_parameters[CIRCLE_JOB]=test-runtest \
     https://circleci.com/api/v1.1/project/bitbucket/${ORGANIZATION_NAME}/${REPOSITORY_NAME}/tree/master
