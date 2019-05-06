# CloudComputingProject
# Exhaustive YouTube Video Analysis using Hadoop Mapreduce and Real-time Sentiment Analysis using Spark Streaming

This project has two parts:
1. Large scale analysis of Youtube videos, providing functionalities like top liked, top disliked, top viewed videos and top hot categories.
2. Real time sentiment analysis of Youtube video comments.

## Guidelines to run the project:
### For Part 1
1. Create a cluster on Cloud Platform.
2. Upload the JAR files on the master node, and setup Hadoop FS.
3. Submit the jobs
4. See the top N results using bash

### For Part 2
1. Setup Zookeeper and Kafka servers on local machine. Instructions: https://kafka.apache.org/quickstart (Change any configuration from the files in config folder). 
2. Start main.py
3. Start comment_analyze.py.
