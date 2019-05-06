# CloudComputingProject
# Exhaustive YouTube Video Analysis using Hadoop Mapreduce and Real-time Sentiment Analysis using Spark Streaming

This project has two parts:
1. Large scale analysis of Youtube videos, providing functionalities like top liked, top disliked, top viewed videos and top hot categories.
2. Real time sentiment analysis of Youtube video comments.

## Guidelines to run the project:
### For Part 1
1. Create a cluster on Cloud Platform. We selected Google Cloud Platform. Choose the configuration(1 master, N workers).
2. Follow the below steps to create jar file and upload on Bucket.\
    hadoop fs -mkdir -p /user/username\
    export PATH=${JAVA_HOME}/bin:${PATH} \
    export HADOOP_CLASSPATH=${JAVA_HOME}/lib/tools.jar\
    hadoop com.sun.tools.javac.Main ./filename.java\
    jar cf jarname.jar filename*.class\
    hadoop fs -copyFromLocal ./jarname.jar\
    hadoop fs -cp ./jarname.jar bucket path\

3. Submit the jobs
4. See the top N results using bash command.

### For Part 2
1. Setup Zookeeper and Kafka servers on local machine. Instructions: https://kafka.apache.org/quickstart (Change any configuration from the files in config folder). 
2. Enable Youtube API and paste the key in the code in order to enable it to extract the comments from the video.
2. Start main.py (It is the main file that starts extracting the Youtube comments for the given query and starts the Kafka producer to inject into Spark stream) 
3. Submit spark job comment_analyze.py. (Command: spark-submit --jars <*list of jars separated by comma*> comment_analyze.py) \
    (This file contains code for creating Spark dstreams and comment analysis).
