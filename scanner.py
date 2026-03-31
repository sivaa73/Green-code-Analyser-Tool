import ast
import os

class EcoScanner(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_For(self, node):
        # RULE 1: Detect Nested Loops (Potential Energy Wasters)
        for child in ast.walk(node):
            if isinstance(child, ast.For) and child is not node:
                self.issues.append({
                    "type": "Nested Loop",
                    "line": child.lineno,
                    "desc": "Nested loops multiply CPU cycles, increasing energy consumption."
                })
        self.generic_visit(node)

    def visit_Call(self, node):
        # RULE 2: Detect repetitive .append() calls in a loop
        # These are often replaceable by faster List Comprehensions
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'append':
            self.issues.append({
                "type": "Inefficient List Growth",
                "line": node.lineno,
                "desc": "Repeated .append() calls can often be replaced by energy-efficient List Comprehensions."
            })
        self.generic_visit(node)

def run_scan(file_path):
    """Parses a Python file and returns a list of detected energy issues."""
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, "r") as f:
        try:
            tree = ast.parse(f.read())
            scanner = EcoScanner()
            scanner.visit(tree)
            return scanner.issues
        except Exception as e:
            print(f"❌ Error parsing {file_path}: {e}")
            return []

if __name__ == "__main__":
    # Self-test: run 'python scanner.py' to check its logic
    test_results = run_scan("target_code.py")
    if test_results:
        print(f"🔎 Detected {len(test_results)} bottlenecks:")
        for issue in test_results:
            print(f"- {issue['type']} at line {issue['line']}")
    else:
        print("✅ No issues found in target_code.py")