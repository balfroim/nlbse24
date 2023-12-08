import dotenv
import os

dotenv.load_dotenv()
DEFECTS4J_HOME = os.getenv("DEFECTS4J_HOME")
CODEQL_HOME = os.getenv("CODEQL_HOME")
DATASET_PATH = "./data/defects4j-bugs.json"
QUERIES_MIDDLE_PATH = ("codeql", "java", "ql", "src", "99_Custom")
