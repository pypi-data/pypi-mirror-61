from . import WMLDeployment
import os


class GermanCreditRisk(WMLDeployment):
    def __init__(self):
        super(GermanCreditRisk, self).__init__(
            name="AIOS Spark Credit Risk deployment xFg",
            asset_name="AIOS Spark Credit Risk model xFg"
        )

    def publish_model(self):
        from pyspark import SparkContext, SQLContext
        from pyspark.ml import Pipeline
        from pyspark.ml.classification import RandomForestClassifier
        from pyspark.ml.evaluation import BinaryClassificationEvaluator
        from pyspark.ml.feature import StringIndexer, VectorAssembler, IndexToString

        ctx = SparkContext.getOrCreate()
        sc = SQLContext(ctx)

        spark_df = sc.read.format(
            "com.databricks.spark.csv").option(
            "header", "true").option(
            "delimiter", ",").option(
            "inferSchema", "true").load(
            os.path.join(os.curdir, 'datasets', 'German_credit_risk', 'credit_risk_training.csv'))

        spark_df.printSchema()

        (train_data, test_data) = spark_df.randomSplit([0.8, 0.2], 24)
        print("Number of records for training: " + str(train_data.count()))
        print("Number of records for evaluation: " + str(test_data.count()))

        si_CheckingStatus = StringIndexer(inputCol='CheckingStatus', outputCol='CheckingStatus_IX')
        si_CreditHistory = StringIndexer(inputCol='CreditHistory', outputCol='CreditHistory_IX')
        si_LoanPurpose = StringIndexer(inputCol='LoanPurpose', outputCol='LoanPurpose_IX')
        si_ExistingSavings = StringIndexer(inputCol='ExistingSavings', outputCol='ExistingSavings_IX')
        si_EmploymentDuration = StringIndexer(inputCol='EmploymentDuration', outputCol='EmploymentDuration_IX')
        si_Sex = StringIndexer(inputCol='Sex', outputCol='Sex_IX')
        si_OthersOnLoan = StringIndexer(inputCol='OthersOnLoan', outputCol='OthersOnLoan_IX')
        si_OwnsProperty = StringIndexer(inputCol='OwnsProperty', outputCol='OwnsProperty_IX')
        si_InstallmentPlans = StringIndexer(inputCol='InstallmentPlans', outputCol='InstallmentPlans_IX')
        si_Housing = StringIndexer(inputCol='Housing', outputCol='Housing_IX')
        si_Job = StringIndexer(inputCol='Job', outputCol='Job_IX')
        si_Telephone = StringIndexer(inputCol='Telephone', outputCol='Telephone_IX')
        si_ForeignWorker = StringIndexer(inputCol='ForeignWorker', outputCol='ForeignWorker_IX')
        si_Label = StringIndexer(inputCol="Risk", outputCol="label").fit(spark_df)
        label_converter = IndexToString(inputCol="prediction", outputCol="predictedLabel", labels=si_Label.labels)

        va_features = VectorAssembler(
            inputCols=["CheckingStatus_IX", "CreditHistory_IX", "LoanPurpose_IX", "ExistingSavings_IX",
                       "EmploymentDuration_IX", "Sex_IX", "OthersOnLoan_IX", "OwnsProperty_IX",
                       "InstallmentPlans_IX",
                       "Housing_IX", "Job_IX", "Telephone_IX", "ForeignWorker_IX", "LoanDuration", "LoanAmount",
                       "InstallmentPercent", "CurrentResidenceDuration", "LoanDuration", "Age",
                       "ExistingCreditsCount",
                       "Dependents"], outputCol="features")

        classifier = RandomForestClassifier(featuresCol="features")

        pipeline = Pipeline(
            stages=[si_CheckingStatus, si_CreditHistory, si_EmploymentDuration, si_ExistingSavings,
                    si_ForeignWorker,
                    si_Housing, si_InstallmentPlans, si_Job, si_LoanPurpose, si_OthersOnLoan,
                    si_OwnsProperty, si_Sex, si_Telephone, si_Label, va_features, classifier, label_converter])

        model = pipeline.fit(train_data)
        predictions = model.transform(test_data)
        evaluator = BinaryClassificationEvaluator(rawPredictionCol="prediction")
        auc = evaluator.evaluate(predictions)

        print("Accuracy = %g" % auc)

        train_data_schema = spark_df.schema
        label_field = next(f for f in train_data_schema.fields if f.name == "Risk")
        label_field.metadata['values'] = si_Label.labels
        input_fileds = filter(lambda f: f.name != "Risk", train_data_schema.fields)

        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: "{}".format(self.asset_name),
                self.wml_client.repository.ModelMetaNames.TYPE: "mllib_2.3",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "spark-mllib_2.3"
            }

        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: "{}".format(self.asset_name),
                self.wml_client.repository.ModelMetaNames.EVALUATION_METRICS: [
                    {
                        "name": "AUC",
                        "value": auc,
                        "threshold": 0.8
                    }
                ]
            }

        published_model_details = self.wml_client.repository.store_model(
            model=model,
            meta_props=model_props,
            training_data=train_data,
            pipeline=pipeline)

        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Model published. Details: {}".format(published_model_details))


class GermanCreditRiskTrainingDataRef(WMLDeployment):
    def __init__(self):
        super(GermanCreditRiskTrainingDataRef, self).__init__(
            name="AIOS German Risk TDF deployment xcx",
            asset_name="AIOS German TDF Risk model xcx"
        )

    def publish_model(self):
        from pyspark import SparkContext, SQLContext
        from pyspark.ml import Pipeline
        from pyspark.ml.classification import RandomForestClassifier
        from pyspark.ml.evaluation import BinaryClassificationEvaluator
        from pyspark.ml.feature import StringIndexer, VectorAssembler, IndexToString
        from pyspark.sql.types import StructType, DoubleType, StringType, ArrayType

        db2_credentials = {
            "hostname": "dashdb-entry-yp-dal09-10.services.dal.bluemix.net",
            "password": "89TsmoAN_Sb_",
            "https_url": "https://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:8443",
            "port": 50000,
            "ssldsn": "DATABASE=BLUDB;HOSTNAME=dashdb-entry-yp-dal09-10.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=dash14647;PWD=89TsmoAN_Sb_;Security=SSL;",
            "host": "dashdb-entry-yp-dal09-10.services.dal.bluemix.net",
            "jdbcurl": "jdbc:db2://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50000/BLUDB",
            "uri": "db2://dash14647:89TsmoAN_Sb_@dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50000/BLUDB",
            "db": "BLUDB",
            "dsn": "DATABASE=BLUDB;HOSTNAME=dashdb-entry-yp-dal09-10.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=dash14647;PWD=89TsmoAN_Sb_;",
            "username": "dash14647",
            "ssljdbcurl": "jdbc:db2://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50001/BLUDB:sslConnection=true;"
        }

        training_data_reference = {
            "name": "Credit Risk feedback",
            "connection": db2_credentials,
            "source": {
                "tablename": "CREDIT_RISK_TRAINING",
                "type": "dashdb"
            }
        }

        print("Training data reference:\n{}".format(training_data_reference))


        ctx = SparkContext.getOrCreate()
        sc = SQLContext(ctx)

        spark_df = sc.read.format(
            "com.databricks.spark.csv").option(
            "header", "true").option(
            "delimiter", ",").option(
            "inferSchema", "true").load(
            os.path.join(os.curdir, 'datasets', 'German_credit_risk', 'credit_risk_training.csv'))

        spark_df.printSchema()

        (train_data, test_data) = spark_df.randomSplit([0.8, 0.2], 24)
        print("Number of records for training: " + str(train_data.count()))
        print("Number of records for evaluation: " + str(test_data.count()))

        si_CheckingStatus = StringIndexer(inputCol='CheckingStatus', outputCol='CheckingStatus_IX')
        si_CreditHistory = StringIndexer(inputCol='CreditHistory', outputCol='CreditHistory_IX')
        si_LoanPurpose = StringIndexer(inputCol='LoanPurpose', outputCol='LoanPurpose_IX')
        si_ExistingSavings = StringIndexer(inputCol='ExistingSavings', outputCol='ExistingSavings_IX')
        si_EmploymentDuration = StringIndexer(inputCol='EmploymentDuration', outputCol='EmploymentDuration_IX')
        si_Sex = StringIndexer(inputCol='Sex', outputCol='Sex_IX')
        si_OthersOnLoan = StringIndexer(inputCol='OthersOnLoan', outputCol='OthersOnLoan_IX')
        si_OwnsProperty = StringIndexer(inputCol='OwnsProperty', outputCol='OwnsProperty_IX')
        si_InstallmentPlans = StringIndexer(inputCol='InstallmentPlans', outputCol='InstallmentPlans_IX')
        si_Housing = StringIndexer(inputCol='Housing', outputCol='Housing_IX')
        si_Job = StringIndexer(inputCol='Job', outputCol='Job_IX')
        si_Telephone = StringIndexer(inputCol='Telephone', outputCol='Telephone_IX')
        si_ForeignWorker = StringIndexer(inputCol='ForeignWorker', outputCol='ForeignWorker_IX')
        si_Label = StringIndexer(inputCol="Risk", outputCol="label").fit(spark_df)
        label_converter = IndexToString(inputCol="prediction", outputCol="predictedLabel", labels=si_Label.labels)

        va_features = VectorAssembler(
            inputCols=["CheckingStatus_IX", "CreditHistory_IX", "LoanPurpose_IX", "ExistingSavings_IX",
                       "EmploymentDuration_IX", "Sex_IX", "OthersOnLoan_IX", "OwnsProperty_IX",
                       "InstallmentPlans_IX",
                       "Housing_IX", "Job_IX", "Telephone_IX", "ForeignWorker_IX", "LoanDuration", "LoanAmount",
                       "InstallmentPercent", "CurrentResidenceDuration", "LoanDuration", "Age",
                       "ExistingCreditsCount",
                       "Dependents"], outputCol="features")

        classifier = RandomForestClassifier(featuresCol="features")

        pipeline = Pipeline(
            stages=[si_CheckingStatus, si_CreditHistory, si_EmploymentDuration, si_ExistingSavings,
                    si_ForeignWorker,
                    si_Housing, si_InstallmentPlans, si_Job, si_LoanPurpose, si_OthersOnLoan,
                    si_OwnsProperty, si_Sex, si_Telephone, si_Label, va_features, classifier, label_converter])

        model = pipeline.fit(train_data)
        predictions = model.transform(test_data)
        evaluator = BinaryClassificationEvaluator(rawPredictionCol="prediction")
        auc = evaluator.evaluate(predictions)

        print("Accuracy = %g" % auc)

        train_data_schema = spark_df.schema
        label_field = next(f for f in train_data_schema.fields if f.name == "Risk")
        label_field.metadata['values'] = si_Label.labels
        input_fileds = filter(lambda f: f.name != "Risk", train_data_schema.fields)

        output_data_schema = StructType(list(input_fileds)). \
            add("prediction", DoubleType(), True, {'modeling_role': 'prediction'}). \
            add("predictedLabel", StringType(), True,
                {'modeling_role': 'decoded-target', 'values': si_Label.labels}). \
            add("probability", ArrayType(DoubleType()), True, {'modeling_role': 'probability'})

        if self.wml_v4:
            training_data_references_v4 = [
                {
                    "type": "db2",
                    "connection": {
                        "url": training_data_reference['connection']['jdbcurl'],
                        "host": training_data_reference['connection']['hostname'],
                        "db": training_data_reference['connection']['db'],
                        "username": training_data_reference['connection']['username'],
                        "password": training_data_reference['connection']['password']
                    },
                    "location": {
                        "tablename": training_data_reference['source']['tablename']
                    }
                }
            ]

            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: "{}".format(self.asset_name),
                # self.wml_client.repository.ModelMetaNames.TRAINING_DATA_REFERENCES: training_data_references_v4,
                self.wml_client.repository.ModelMetaNames.TYPE: "mllib_2.3",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "spark-mllib_2.3",
                self.wml_client.repository.ModelMetaNames.OUTPUT_DATA_SCHEMA: output_data_schema.jsonValue(),
            }

        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: "{}".format(self.asset_name),
                self.wml_client.repository.ModelMetaNames.TRAINING_DATA_REFERENCE: training_data_reference,
                self.wml_client.repository.ModelMetaNames.OUTPUT_DATA_SCHEMA: output_data_schema.jsonValue(),
                self.wml_client.repository.ModelMetaNames.EVALUATION_METRICS: [
                    {
                        "name": "AUC",
                        "value": auc,
                        "threshold": 0.8
                    }
                ]
            }

        published_model_details = self.wml_client.repository.store_model(
            model=model,
            meta_props=model_props,
            training_data=train_data,
            pipeline=pipeline)

        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Model published. Details: {}".format(published_model_details))


class Drug(WMLDeployment):
    def __init__(self):
        super(Drug, self).__init__(
            name="AIOS Spark Drugs feedback deployment",
            asset_name="AIOS Spark Drugs feedback model"
        )

    def publish_model(self):
        from pyspark import SparkContext, SQLContext
        from pyspark.ml import Pipeline
        from pyspark.ml.classification import DecisionTreeClassifier
        from pyspark.ml.evaluation import MulticlassClassificationEvaluator
        from pyspark.ml.feature import StringIndexer, VectorAssembler, IndexToString
        from pyspark.sql.types import StructType, DoubleType, StringType, ArrayType
        from datetime import datetime

        ctx = SparkContext.getOrCreate()
        sc = SQLContext(ctx)

        db2_credentials = {
            "hostname": "dashdb-entry-yp-dal09-10.services.dal.bluemix.net",
            "password": "89TsmoAN_Sb_",
            "https_url": "https://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:8443",
            "port": 50000,
            "ssldsn": "DATABASE=BLUDB;HOSTNAME=dashdb-entry-yp-dal09-10.services.dal.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=dash14647;PWD=89TsmoAN_Sb_;Security=SSL;",
            "host": "dashdb-entry-yp-dal09-10.services.dal.bluemix.net",
            "jdbcurl": "jdbc:db2://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50000/BLUDB",
            "uri": "db2://dash14647:89TsmoAN_Sb_@dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50000/BLUDB",
            "db": "BLUDB",
            "dsn": "DATABASE=BLUDB;HOSTNAME=dashdb-entry-yp-dal09-10.services.dal.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=dash14647;PWD=89TsmoAN_Sb_;",
            "username": "dash14647",
            "ssljdbcurl": "jdbc:db2://dashdb-entry-yp-dal09-10.services.dal.bluemix.net:50001/BLUDB:sslConnection=true;"
        }

        training_data_reference = {
            "name": "DRUG feedback",
            "connection": db2_credentials,
            "source": {
                "tablename": "DRUG_FEEDBACK_DATA",
                "type": "dashdb"
            }
        }

        train_data = sc.read.format("com.databricks.spark.csv").option("header", "true").option("delimiter",
                                                                                                ";").option(
            "inferSchema", "true").load(os.path.join(os.curdir, 'datasets', 'drugs', 'drug_feedback_data.csv'))
        test_data = sc.read.format("com.databricks.spark.csv").option("header", "true").option("delimiter", ";").option(
            "inferSchema", "true").load(os.path.join(os.curdir, 'datasets', 'drugs', 'drug_feedback_test.csv'))
        stringIndexer_sex = StringIndexer(inputCol='SEX', outputCol='SEX_IX')
        stringIndexer_bp = StringIndexer(inputCol='BP', outputCol='BP_IX')
        stringIndexer_chol = StringIndexer(inputCol='CHOLESTEROL', outputCol='CHOLESTEROL_IX')
        stringIndexer_label = StringIndexer(inputCol="DRUG", outputCol="label").fit(train_data)
        vectorAssembler_features = VectorAssembler(inputCols=["AGE", "SEX_IX", "BP_IX", "CHOLESTEROL_IX", "NA", "K"],
                                                   outputCol="features")
        dt = DecisionTreeClassifier(labelCol="label", featuresCol="features")
        labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel",
                                       labels=stringIndexer_label.labels)
        pipeline = Pipeline(stages=[stringIndexer_label, stringIndexer_sex, stringIndexer_bp, stringIndexer_chol,
                                       vectorAssembler_features, dt, labelConverter])

        model = pipeline.fit(train_data)
        predictions = model.transform(test_data)
        evaluatorDT = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction",
                                                        metricName="accuracy")
        accuracy = evaluatorDT.evaluate(predictions)

        print("Accuracy = %g" % accuracy)

        train_data_schema = train_data.schema
        label_field = next(f for f in train_data_schema.fields if f.name == "DRUG")
        label_field.metadata['values'] = stringIndexer_label.labels

        input_fileds = filter(lambda f: f.name != "DRUG", train_data_schema.fields)

        output_data_schema = StructType(list(input_fileds)). \
            add("prediction", DoubleType(), True, {'modeling_role': 'prediction'}). \
            add("predictedLabel", StringType(), True,
                {'modeling_role': 'decoded-target', 'values': stringIndexer_label.labels}). \
            add("probability", ArrayType(DoubleType()), True, {'modeling_role': 'probability'})

        if self.wml_v4:
            print("Publishing new model using V4 client.")
            training_data_references_v4 = [
                {
                    "type": "db_2",
                    "connection": {
                        "host": training_data_reference['connection']['hostname'],
                        "db": training_data_reference['connection']['db'],
                        "username": training_data_reference['connection']['username'],
                        "password": training_data_reference['connection']['password']
                    },
                    "location": {
                        "tablename": training_data_reference['source']['tablename']
                    }
                }
            ]

            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: "{}".format(self.asset_name),
                # self.wml_client.repository.ModelMetaNames.TRAINING_DATA_REFERENCE: training_data_reference_v4,
                self.wml_client.repository.ModelMetaNames.TYPE: "mllib_2.3",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "spark-mllib_2.3",
                self.wml_client.repository.ModelMetaNames.METRICS: [
                    {
                        "timestamp": datetime.now(),
                        "name": "accuracy",
                        "value": 0.7,
                        "threshold": 0.8
                    }
                ]
            }

        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: "{}".format(self.asset_name),
                self.wml_client.repository.ModelMetaNames.TRAINING_DATA_REFERENCE: training_data_reference,
                self.wml_client.repository.ModelMetaNames.EVALUATION_METHOD: "multiclass",
                self.wml_client.repository.ModelMetaNames.EVALUATION_METRICS: [
                    {
                        "name": "accuracy",
                        "value": 0.7,
                        "threshold": 0.8
                    }
                ]
            }

        published_model_details = self.wml_client.repository.store_model(
            model=model,
            meta_props=model_props,
            training_data=train_data,
            pipeline=pipeline)

        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Model published. Details: {}".format(published_model_details))


class RegressionCustomerSatisfaction(WMLDeployment):
    def __init__(self):
        super(RegressionCustomerSatisfaction, self).__init__(
            name="AIOS Spark Regression Customer Satisfaction deployment",
            asset_name="AIOS Spark Regression Customer Satisfaction model"
        )

    def publish_model(self):
        from pyspark.ml import Pipeline
        from pyspark.ml.feature import RFormula
        from pyspark.ml.regression import LinearRegression
        from pyspark.sql import SparkSession
        from pyspark.sql.types import StructType, DoubleType, ArrayType

        file_path = os.path.join(os.getcwd(), 'datasets', 'SparkMlibRegression', 'WA_FnUseC_TelcoCustomerChurn.csv')

        spark = SparkSession.builder.getOrCreate()

        df_data = spark.read \
            .format('org.apache.spark.sql.execution.datasources.csv.CSVFileFormat') \
            .option('header', 'true') \
            .option('inferSchema', 'true') \
            .option('nanValue', ' ') \
            .option('nullValue', ' ') \
            .load(file_path)

        df_complete = df_data.dropna()
        df_complete.drop('Churn')

        (train_data, test_data) = df_complete.randomSplit([0.8, 0.2], 24)

        features = RFormula(
            formula="~ gender + SeniorCitizen +  Partner + Dependents + tenure + PhoneService + MultipleLines + "
                    "InternetService + OnlineSecurity + OnlineBackup + DeviceProtection + TechSupport + StreamingTV + "
                    "StreamingMovies + Contract + PaperlessBilling + PaymentMethod + MonthlyCharges - 1")

        lr = LinearRegression(labelCol='TotalCharges')
        pipeline_lr = Pipeline(stages=[features, lr])
        lr_model = pipeline_lr.fit(train_data)
        lr_predictions = lr_model.transform(test_data)

        output_data_schema = StructType(list(filter(lambda f: f.name != "TotalCharges", df_data.schema.fields))). \
            add("prediction", DoubleType(), True, {'modeling_role': 'prediction'}). \
            add("probability", ArrayType(DoubleType()), True, {'modeling_role': 'probability'})

        model = lr_model
        pipeline = pipeline_lr
        training_data = train_data
        test_data = test_data
        prediction = lr_predictions
        print("Predictions: {}".format(prediction))
        output_data_schema = output_data_schema.jsonValue()

        if self.wml_v4:
            print("Publishing new model using V4 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name,
                self.wml_client.repository.ModelMetaNames.TYPE: "mllib_2.3",
                self.wml_client.repository.ModelMetaNames.RUNTIME_UID: "spark-mllib_2.3"
            }

        else:
            print("Publishing new model using V3 client.")
            model_props = {
                self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
                self.wml_client.repository.ModelMetaNames.NAME: self.asset_name
            }

        published_model_details = self.wml_client.repository.store_model(model=model,
                                                                         meta_props=model_props,
                                                                         training_data=training_data,
                                                                         pipeline=pipeline)

        self.asset_uid = self.wml_client.repository.get_model_uid(published_model_details)

        print("Model published. Details: {}".format(published_model_details))

