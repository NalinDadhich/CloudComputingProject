import java.io.IOException;

import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.log4j.BasicConfigurator;

public class TopCategoriesPerYear extends Configured implements Tool{

	public static class Map extends Mapper<LongWritable, Text, Text, LongWritable> {
		@Override
		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			String line = value.toString();
			String[] lineArr = line.split("\t");
			String cat = lineArr[5];
			Long views = Long.parseLong(lineArr[1]);
			context.write(new Text(cat), new LongWritable(views));
		}
	}
	
	public static class Reduce extends Reducer<Text, LongWritable, Text, LongWritable> 
	{
		@Override
		public void reduce(Text key, Iterable<LongWritable> values, Context context) throws IOException, InterruptedException {
			
			long total = 0;

			for(LongWritable value :values){
				// context.write(key, value);
				total += value.get();
			}
			context.write(key, new LongWritable(total));
		}
	}

	public int run(String[] args) throws Exception {
		Configuration conf= new Configuration();
		

		Job job = new Job(conf,"TopCategories");
		
		job.setJarByClass(TopCategoriesPerYear.class);
		job.setMapperClass(Map.class);
		// job.setReducerClass(Reduce.class);
		
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(LongWritable.class);
		
		// job.setInputFormatClass(Text.class);
		// job.setOutputFormatClass(Text.class);
	        
	    FileInputFormat.addInputPath(job, new Path(args[0]));
	    FileInputFormat.setInputDirRecursive(job, true);
	    FileOutputFormat.setOutputPath(job, new Path(args[1]));
		System.out.println("See output in folder: " + args[1]);
		long startTime = System.currentTimeMillis();
		boolean success = job.waitForCompletion(true);
		System.out.println("Time elapsed (sec) = " + (System.currentTimeMillis() - startTime) / 1000.0);
		return success ? 0 : 1;
		
	}

	public static void main(String[] args) throws Exception {
		TopCategoriesPerYear driver = new TopCategoriesPerYear();
		int exitCode = ToolRunner.run(driver, args);
		System.exit(exitCode);
	}
	
}