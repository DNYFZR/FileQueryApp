# Install Python image
FROM python:3.10

# Set base dir
WORKDIR /

# Copy requirements to image dir (enables Docker caching)
COPY /.venv/requirements.txt /requirements.txt

# Update pip and install requirements
RUN python -m pip install --no-cache-dir --upgrade pip -r /requirements.txt

# Copy repo to image
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Set-up Streamlit
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
	[server]\n\
	enableCORS = false\n\
	" > /root/.streamlit/config.toml'

# Add port for Streamlit
EXPOSE 8501

# Run 
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
CMD ["streamlit", "run", "--server.port", "8501", "app.py"]
