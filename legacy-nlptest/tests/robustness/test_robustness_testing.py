import unittest
import os
from nlptest.robustness.robustness_testing import test_robustness
import sparknlp
from sparknlp.annotator import *
from pyspark.ml import Pipeline


class TestRobustnessTesting(unittest.TestCase):

    def setUp(self):
        THIS_DIR = os.path.dirname(os.path.abspath(__file__))

        # Create a SparkSession object
        self.spark = sparknlp.start()

        # Create a pipeline model object
        document_assembler = DocumentAssembler() \
            .setInputCol("text") \
            .setOutputCol("document")

        tokenizer = Tokenizer() \
            .setInputCols(["document"]) \
            .setOutputCol("token")

        embeddings = WordEmbeddingsModel.pretrained('glove_100d') \
            .setInputCols(["document", 'token']) \
            .setOutputCol("embeddings")

        ner = NerDLModel.pretrained("ner_dl", 'en') \
            .setInputCols(["document", "token", "embeddings"]) \
            .setOutputCol("ner")

        ner_pipeline = Pipeline().setStages([document_assembler, tokenizer, embeddings, ner])

        self.pipeline_model = ner_pipeline.fit(self.spark.createDataFrame([[""]]).toDF("text"))

        # Set the test file path
        self.test_file_path = os.path.join(THIS_DIR, os.pardir, 'resources/test.conll')

    def test_dict_and_keys(self):
        # Test robustness using default parameters
        robustness_test_results = test_robustness(spark=self.spark, pipeline_model=self.pipeline_model,
                                                  test_file_path=self.test_file_path)

        # Assert that the test_robustness function returns a dictionary
        self.assertIsInstance(robustness_test_results, dict)

        # Assert that test_robustness output has keys 'metrics', 'comparison_df', and 'test_details' in the dictionary
        self.assertIn('metrics', robustness_test_results)
        self.assertIn('comparison_df', robustness_test_results)
        self.assertIn('test_details', robustness_test_results)

        # Assert that test_robustness 'metrics' output has keys for each perturbation
        for test_name in ['capitalization_upper', 'capitalization_lower', 'capitalization_title',
                          'add_punctuation', 'strip_punctuation', 'introduce_typos', 'add_contractions', 'add_context',
                          'american_to_british', 'swap_entities', 'swap_cohyponyms']:

            self.assertIn(test_name, robustness_test_results['metrics'])

    def test_invalid_test_type(self):
        # Test when an invalid test type is specified
        with self.assertRaises(ValueError):
            test_robustness(self.spark, self.pipeline_model, self.test_file_path, test=['invalid'])

    def test_invalid_metrics_output_format(self):
        # Test when an invalid metrics output format is specified
        with self.assertRaises(ValueError):
            test_robustness(self.spark, self.pipeline_model, self.test_file_path, metrics_output_format='invalid')


if __name__ == '__main__':
    unittest.main()