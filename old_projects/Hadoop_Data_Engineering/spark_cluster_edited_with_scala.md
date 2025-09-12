
# Hadoop, YARN, Spark installation and configurations #
/ Created a specific superuser named hadoop for this assignment, on a VM running Ubuntu 20.04
/ Versions used: Hadoop 3.3.6, spark-3.5.0-bin-hadoop3, hbase-2.5.5, java-11-openjdk-amd64

/ First let's establish a password-less SSH connection saved in /home/hadoop/.ssh/ as id_rsa.pub <br />
```console
ssh hadoop@localhost
ssh-keygen -t rsa
```


/ add the created key to the authorized keys file <br />
```console
cat .ssh/id_rsa.pub >> .ssh/authorized_keys
```

/ Let's start with Hadoop's configuration <br />
/ specify HDFS as the default file system and the Hadoop cluster's namenode address <br />
```console
nano ~/hadoop/etc/hadoop/core-site.xml
```

/ Defining single-cluster node <br />
/ define a replication factor "1", as the dfs is running in a single VM, and also define the paths for namenode & datanode <br />
```console
nano ~/hadoop/etc/hadoop/hdfs-site.xml
```

/ of course we need to create the respective paths and folders for namenode & datanode <br />
```console
mkdir /home/hadoop/hadoopdata/hdfs/namenode/
mkdir /home/hadoop/hadoopdata/hdfs/datanode/
```


/ now let's proceed with defining the Java path for each appropriate environment file <br />
```console
nano ~/hadoop/etc/hadoop/hadoop-env.sh
```
/ add java path location <br />
```console
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

/ before initiating HDFS for the first time let's format the name node <br />
```console
~/hadoop/bin/hdfs namenode -format
```


/ YARN & Map Reduce configuration <br />
/ specify the properties as found in hadoop documentation, some additional properties can be set for system resources <br />
```console
nano ~/hadoop/etc/hadoop/yarn-site.xml
nano ~/hadoop/etc/hadoop/mapred-site.xml
```

/ next step is to initiate the following and also check with our browser that the services are active <br />
```console
~/hadoop/sbin/start-dfs.sh
~/hadoop/sbin/start-yarn.sh
```

/ visit the following addresses in browser <br />
```console
http://localhost:9870
http://localhost:8088
```

/ now we are ready to interact with HDFS and check the root directory
```console
~/hadoop/bin/hdfs dfs -ls
```

/let's also copy the csv files to a specific folder under root directory and also a folder for our parquet output
```console
~/hadoop/bin/hdfs dfs -mkdir /trans_data
~/hadoop/bin/hdfs dfs -mkdir /output
~/hadoop/bin/hdfs dfs -put ~/cvas_data_transactions.csv /trans_data/
~/hadoop/bin/hdfs dfs -put ~/subscribers.csv /trans_data/
```


/ Later on we proceed with the installation of Spark and doing the appropriate configurations
/ after completing the installation we navigate to the "conf" folder of Spark and create a file based on Spark's environment template
```console
nano ~/spark-3.5.0-bin-hadoop3/conf/spark-env.sh
```

/ add the following
```console
export HADOOP_CONF_DIR=/home/hadoop/hadoop/etc/hadoop/
export YARN_CONF_DIR=/home/hadoop/hadoop/etc/hadoop/
export PYSPARK_PYTHON=python3
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

/ I also created a separate file for the workers based on workers.template
```console
cp ~/spark-3.5.0-bin-hadoop3/conf/workers.template ~/spark-3.5.0-bin-hadoop3/conf/workers
```


/ We are ready now to initiate spark-shell and start our processes and move on to SCALA environment
```console
~/spark-3.5.0-bin-hadoop3/bin/spark-shell --master yarn
```

/ I have also edited the csv files and added headers as per assignment's description


# SCALA #
/ using the following commands in spark shell we get the result parquet files /
```scala
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types._
import org.apache.hadoop.hbase.{HBaseConfiguration, HTableDescriptor, TableName}
import org.apache.hadoop.hbase.client.{Connection, ConnectionFactory, Put}
import org.apache.hadoop.hbase.mapreduce.TableInputFormat
import org.apache.hadoop.hbase.util.Bytes
```

// Create a SparkSession
```scala
val spark = SparkSession.builder()
  .appName("CSV_parquet_to_HBase")
  .getOrCreate()
```

// Define the custom schema for subscribers
```scala
val subscribersSchema = new StructType()
  .add(StructField("subscriber_id", StringType, true))
  .add(StructField("activation_date", DateType, true))
```

// Read the subscribers CSV file with the defined schema
```scala
val subscribersDF = spark.read
  .schema(subscribersSchema)
  .option("delimiter", ",")
  .option("header", "true")
  .csv("hdfs:///trans_data/subscribers.csv")
```

// Filter out records that don't comply with the schema
```scala
val validSubscribersDF = subscribersDF.filter($"subscriber_id".isNotNull && $"activation_date".isNotNull)
```

// Define a function to generate the HBase row key
```scala
val generateRowKey = udf((subscriber_id: String, activation_date: String) => {
  s"${subscriber_id}${activation_date}"
})
```

// Add a new column with the generated row key
```scala
val subscribersWithRowKey = validSubscribersDF
  .withColumn("row_key", generateRowKey($"subscriber_id", $"activation_date"))
```

// Configure HBase connection
```scala
val hbaseConf = HBaseConfiguration.create()
hbaseConf.set(TableInputFormat.INPUT_TABLE, "final_parquet")
```

// Function to write records to HBase
```scala
def writeToHBase(row: org.apache.spark.sql.Row): Unit = {
  val connection: Connection = ConnectionFactory.createConnection(hbaseConf)
  val table = connection.getTable(TableName.valueOf("final_parquet"))

  val put = new Put(Bytes.toBytes(row.getAs[String]("row_key")))
  put.addColumn(Bytes.toBytes("sud_id"), Bytes.toBytes("subscriber_id"), Bytes.toBytes(row.getAs[String]("subscriber_id")))
  put.addColumn(Bytes.toBytes("act_dt"), Bytes.toBytes("activation_date"), Bytes.toBytes(row.getAs[String]("activation_date")))

  table.put(put)
  table.close()
  connection.close()
}
```

// Write valid subscribers to HBase
```scala
subscribersWithRowKey.foreach(writeToHBase)
```

// Read the transactions CSV file
```scala
val transactionsSchema = new StructType()
  .add(StructField("timestamp", TimestampType, true))
  .add(StructField("sub_id", StringType, true))
  .add(StructField("amount", DecimalType(10, 4), true))
  .add(StructField("channel", StringType, true))

val transactionsDF = spark.read
  .schema(transactionsSchema)
  .option("delimiter", ",")
  .option("header", "true")
  .csv("hdfs:///trans_data/cvas_data_transactions.csv")

val validTransactionsDF = transactionsDF.filter($"timestamp".isNotNull && $"sub_id".isNotNull && $"amount".isNotNull && $"channel".isNotNull)
```

// Join transactions data with subscribers data to obtain the "activation_date" column
```scala
val joinedDF = validTransactionsDF.join(subscribersWithRowKey, Seq("sub_id"), "left")
```

// Specify the path for the Parquet output
```scala
val parquetOutputPath = "hdfs:///output/transactions.parquet"
```

// Write the joined DataFrame to Parquet
```scala
joinedDF.write.parquet(parquetOutputPath)
```

// Stop the SparkSession when done
```scala
spark.stop()
```
