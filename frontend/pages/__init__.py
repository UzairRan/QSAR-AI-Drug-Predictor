"""
Pages module initialization
"""

from .predict import render as render_predict
from .batch_predict import render as render_batch
from .explain import render as render_explain
from .about_model import render as render_about

# Define page variables for app.py imports
predict_page = render_predict
batch_predict_page = render_batch
explain_page = render_explain
about_model_page = render_about   