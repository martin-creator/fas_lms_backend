import os
import sys
import ast
from django.apps import apps
from graphviz import Digraph, ExecutableNotFound

# Set up your Django project settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
import django
django.setup()

def find_model_files():
    """Find and return a list of model files in the Django project."""
    model_files = []
    for app in apps.get_app_configs():
        app_path = app.path
        model_file = os.path.join(app_path, 'models.py')
        if os.path.exists(model_file):
            model_files.append(model_file)
    return model_files

def extract_model_relations(model_file):
    """Extract and return model relations from a given models.py file."""
    with open(model_file, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=model_file)

    class ModelVisitor(ast.NodeVisitor):
        def __init__(self):
            self.models = {}

        def visit_ClassDef(self, node):
            if any(base.attr == 'Model' for base in node.bases if isinstance(base, ast.Attribute)):
                self.models[node.name] = []
                for stmt in node.body:
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if isinstance(target, ast.Name):
                                field_name = target.id
                                if isinstance(stmt.value, ast.Call):
                                    field_type = get_field_type(stmt.value)
                                    if field_type:
                                        related_model = get_related_model(stmt.value)
                                        if related_model:
                                            self.models[node.name].append((field_name, field_type, related_model))

    def get_field_type(value):
        if isinstance(value.func, ast.Attribute):
            return value.func.attr
        elif isinstance(value.func, ast.Name):
            return value.func.id
        return None

    def get_related_model(value):
        if value.args and isinstance(value.args[0], ast.Name):
            return value.args[0].id
        elif value.args and isinstance(value.args[0], ast.Constant):
            return value.args[0].value
        return None

    visitor = ModelVisitor()
    visitor.visit(tree)
    return visitor.models

def generate_textual_representation(models_relations):
    """Generate a textual representation of the model relations."""
    representation = ""
    for model, relations in models_relations.items():
        representation += f"{model}\n"
        for relation in relations:
            representation += f" └── {relation[0]} ({relation[1]}) -> {relation[2]}\n"
        representation += "\n"  # Add an extra newline after each model's relations

    return representation

def generate_uml_diagram(models_relations, output_file='uml_diagram'):
    """Generate a UML diagram of the model relations and save it as a PNG file."""
    dot = Digraph(comment='UML Diagram')

    for model, relations in models_relations.items():
        dot.node(model, model, shape='box')
        for relation in relations:
            dot.edge(model, relation[2], label=f"{relation[0]} ({relation[1]})")
    
    try:
        dot.render(output_file, format='png')
    except ExecutableNotFound:
        print("Graphviz 'dot' executable not found. Please ensure Graphviz is installed and the PATH is set correctly.")
        sys.exit(1)

def generate_comprehensive_visualization(models_relations, output_file='comprehensive_visualization'):
    """Generate a comprehensive visualization of the model relations in a custom format."""
    dot = Digraph(comment='Comprehensive Visualization')

    for model, relations in models_relations.items():
        with dot.subgraph(name=f"cluster_{model}") as c:
            c.attr(label=model, shape='box', style='filled', color='lightgrey')
            c.node(model, model)
            for relation in relations:
                c.edge(model, relation[2], label=f"{relation[0]} ({relation[1]})", style='dotted')
    
    try:
        dot.render(output_file, format='png')
    except ExecutableNotFound:
        print("Graphviz 'dot' executable not found. Please ensure Graphviz is installed and the PATH is set correctly.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py [text|uml|comprehensive]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    model_files = find_model_files()
    all_models_relations = {}
    for model_file in model_files:
        models_relations = extract_model_relations(model_file)
        if models_relations:
            all_models_relations.update(models_relations)
    
    if command == "text":
        representation = generate_textual_representation(all_models_relations)
        with open('models_representation.md', 'w', encoding='utf-8') as f:
            f.write(representation)
        print("Textual representation written to models_representation.md")
    
    elif command == "uml":
        generate_uml_diagram(all_models_relations, output_file='uml_diagram')
        print("UML diagram written to uml_diagram.png")
    
    elif command == "comprehensive":
        generate_comprehensive_visualization(all_models_relations, output_file='comprehensive_visualization')
        print("Comprehensive visualization written to comprehensive_visualization.png")
    
    else:
        print("Invalid command. Use 'text', 'uml', or 'comprehensive'.")
