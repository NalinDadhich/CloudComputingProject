import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.util.ToolRunner;

public class TopDisLikedVideos{

	public static class Map extends Mapper<LongWritable, Text, Text, LongWritable> {
		@Override
		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			String line = value.toString();
			String[] lineArr = line.split("\t");
			String videoID = lineArr[0];
			Long dislikes = Long.parseLong(lineArr[3]);
			context.write(new Text(videoID), new LongWritable(dislikes));
		}
	}
	
	public static class Reduce extends Reducer<Text, LongWritable, Text, LongWritable> 
	{
		@Override
		public void reduce(Text key, Iterable<LongWritable> values, Context context) throws IOException, InterruptedException {
			
			long total = 0;

			for(LongWritable value :values){
				total += value.get();
			}
			context.write(key, new LongWritable(total));
		}
	}

	public static void main(String[] args) throws Exception {
		Configuration conf= new Configuration();
		

		Job job = new Job(conf,"TopDisLiked");
		
		job.setJarByClass(TopCategoriesPerYear.class);
		job.setMapperClass(Map.class);
		job.setReducerClass(Reduce.class);
		
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(LongWritable.class);
		
		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileInputFormat.setInputDirRecursive(job, true);
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		System.out.println("See output in folder: " + args[1]);
		
		long startTime = System.currentTimeMillis();
		boolean success = job.waitForCompletion(true);
		System.out.println("Time elapsed (sec) = " + (System.currentTimeMillis() - startTime) / 1000.0);
		
		System.exit(success ? 0 : 1);
		
	}
	
}