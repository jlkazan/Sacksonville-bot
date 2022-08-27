FROM public.ecr.aws/lambda/python:3.9

# Copy function code
COPY sacksonville_bot/bot.py ${LAMBDA_TASK_ROOT}
COPY sacksonville_bot/.env ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "bot.run_bot" ]