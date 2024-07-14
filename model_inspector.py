import os
import sys
import ast
import inspect
from django.apps import apps
from django.conf import settings
from django.db import models
from graphviz import Digraph

# Set up your Django project settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
import django
django.setup()

def find_model_files():
    model_files = []
    for app in apps.get_app_configs():
        app_path = app.path
        model_file = os.path.join(app_path, 'models.py')
        if os.path.exists(model_file):
            model_files.append(model_file)
    return model_files

def extract_model_relations(model_file):
    with open(model_file, 'r') as f:
        tree = ast.parse(f.read(), filename=model_file)

    class ModelVisitor(ast.NodeVisitor):
        def __init__(self):
            self.models = {}

        def visit_ClassDef(self, node):
            if 'models.Model' in [base.id for base in node.bases if isinstance(base, ast.Name)]:
                self.models[node.name] = []
                for stmt in node.body:
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if isinstance(target, ast.Name):
                                field_name = target.id
                                if isinstance(stmt.value, ast.Call):
                                    field_type = stmt.value.func.attr
                                    if field_type in ('ForeignKey', 'OneToOneField', 'ManyToManyField'):
                                        related_model = stmt.value.args[0].id
                                        self.models[node.name].append((field_name, field_type, related_model))

    visitor = ModelVisitor()
    visitor.visit(tree)
    return visitor.models

def generate_textual_representation(models_relations):
    representation = ""
    for model, relations in models_relations.items():
        representation += f"{model}\n"
        for relation in relations:
            representation += f" └── {relation[0]} ({relation[1]}) -> {relation[2]}\n"
    return representation

def generate_uml_diagram(models_relations, output_file='uml_diagram'):
    dot = Digraph(comment='UML Diagram')

    for model, relations in models_relations.items():
        dot.node(model, model)
        for relation in relations:
            dot.edge(model, relation[2], label=f"{relation[0]} ({relation[1]})")
    
    dot.render(output_file, format='png')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py [text|uml]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    model_files = find_model_files()
    all_models_relations = {}
    for model_file in model_files:
        models_relations = extract_model_relations(model_file)
        all_models_relations.update(models_relations)
    
    if command == "text":
        representation = generate_textual_representation(all_models_relations)
        with open('models_representation.md', 'w') as f:
            f.write(representation)
        print("Textual representation written to models_representation.md")
    
    elif command == "uml":
        generate_uml_diagram(all_models_relations, output_file='uml_diagram')
        print("UML diagram written to uml_diagram.png")
    
    else:
        print("Invalid command. Use 'text' or 'uml'.")
