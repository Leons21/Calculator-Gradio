import gradio as gr
import ast
import operator
import math
from fractions import Fraction

# Operator whitelist
allowed_ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

# Safe Evaluator Function
def safe_eval(expr):
    def _eval(node):
        if isinstance(node, ast.Num):  
            return node.n

        elif isinstance(node, ast.BinOp):  # "+, -, *, /, **""
            if type(node.op) not in allowed_ops:
                raise ValueError("Operator not allowed!")
            return allowed_ops[type(node.op)](_eval(node.left), _eval(node.right))

        elif isinstance(node, ast.UnaryOp):  # negative
            if type(node.op) not in allowed_ops:
                raise ValueError("Unary Operator not Allowed!")
            return allowed_ops[type(node.op)](_eval(node.operand))

        elif isinstance(node, ast.Call): #Function call
            if isinstance(node.func, ast.Name):
                fname = node.func.id.lower()

                # Trigonometry
                if fname == "sin":
                    return math.sin(_eval(node.args[0]))
                elif fname == "cos":
                    return math.cos(_eval(node.args[0]))
                elif fname == "tan":
                    return math.tan(_eval(node.args[0]))

                # square root
                elif fname == "sqrt":
                    return math.sqrt(_eval(node.args[0]))

                else:
                    raise ValueError(f"function! '{fname}' Unknown!")
            else:
                raise ValueError("Format function wrong!")

        else:
            raise ValueError("Expression not valid!")

    parsed = ast.parse(expr, mode="eval")
    return _eval(parsed.body)

# Calculate
def calculate_expression(expr):
    expr = expr.replace("^", "**")
    
    try:
        result = safe_eval(expr)
        return result
    except Exception as e:
        return f"Error: {e}"

# Convert
def convert_to_fraction(result):
    try:
        val = float(result)
        frac = Fraction(val).limit_denominator()
        return f"{frac.numerator}/{frac.denominator}"
    except:
        return "Convert error"

# Keypad
def add_to_expression(expr, value):
    return (expr or "") + value


def clear_expression():
    return ""


def delete_last(expr):
    return expr[:-1] if expr else ""


# UI Gradio
with gr.Blocks(css="""
:root {
  --bg-light: #ffffff;
  --bg-dark: #222222;
  --text-light: #000000;
  --text-dark: #eeeeee;
}

.light-mode {
  background-color: var(--bg-light);
  color: var(--text-light);
  padding: 20px;
  border-radius: 12px;
}

.dark-mode {
  background-color: var(--bg-dark);
  color: var(--text-dark);
  padding: 20px;
  border-radius: 12px;
}
""") as demo:

    theme_state = gr.State("dark")

    title = gr.Markdown("## Calculator")

    container = gr.Column(elem_classes="dark-mode")

    with container:
        expr = gr.Textbox(label="Expression", interactive=True)
        result = gr.Textbox(label="Result", interactive=False)

        # KEYBOARD GRID
        with gr.Row():
            with gr.Column():
                with gr.Row():
                    gr.Button("7").click(add_to_expression, inputs=[expr, gr.State("7")], outputs=expr)
                    gr.Button("8").click(add_to_expression, inputs=[expr, gr.State("8")], outputs=expr)
                    gr.Button("9").click(add_to_expression, inputs=[expr, gr.State("9")], outputs=expr)
                    gr.Button("/").click(add_to_expression, inputs=[expr, gr.State("/")], outputs=expr)

                with gr.Row():
                    gr.Button("4").click(add_to_expression, inputs=[expr, gr.State("4")], outputs=expr)
                    gr.Button("5").click(add_to_expression, inputs=[expr, gr.State("5")], outputs=expr)
                    gr.Button("6").click(add_to_expression, inputs=[expr, gr.State("6")], outputs=expr)
                    gr.Button("*").click(add_to_expression, inputs=[expr, gr.State("*")], outputs=expr)

                with gr.Row():
                    gr.Button("1").click(add_to_expression, inputs=[expr, gr.State("1")], outputs=expr)
                    gr.Button("2").click(add_to_expression, inputs=[expr, gr.State("2")], outputs=expr)
                    gr.Button("3").click(add_to_expression, inputs=[expr, gr.State("3")], outputs=expr)
                    gr.Button("-").click(add_to_expression, inputs=[expr, gr.State("-")], outputs=expr)

                with gr.Row():
                    gr.Button("(").click(add_to_expression, inputs=[expr, gr.State("(")], outputs=expr)
                    gr.Button("0").click(add_to_expression, inputs=[expr, gr.State("0")], outputs=expr)
                    gr.Button(")").click(add_to_expression, inputs=[expr, gr.State(")")], outputs=expr)
                    gr.Button("+").click(add_to_expression, inputs=[expr, gr.State("+")], outputs=expr)

                with gr.Row():
                    gr.Button(".").click(add_to_expression, inputs=[expr, gr.State(".")], outputs=expr)
                    gr.Button("^").click(add_to_expression, inputs=[expr, gr.State("^")], outputs=expr)
                    gr.Button("DEL").click(delete_last, inputs=expr, outputs=expr)
                    gr.Button("CLEAR").click(clear_expression, outputs=expr)

            with gr.Column():
                gr.Button("sin(").click(add_to_expression, inputs=[expr, gr.State("sin(")], outputs=expr)
                gr.Button("cos(").click(add_to_expression, inputs=[expr, gr.State("cos(")], outputs=expr)
                gr.Button("tan(").click(add_to_expression, inputs=[expr, gr.State("tan(")], outputs=expr)
                gr.Button("sqrt(").click(add_to_expression, inputs=[expr, gr.State("sqrt(")], outputs=expr)
                gr.Button("Calculate").click(calculate_expression, inputs=expr, outputs=result)
                gr.Button("Dec → Fraction").click(convert_to_fraction, inputs=result, outputs=result)
                toggle_btn = gr.Button("Theme (Light/Dark)")

    # Theme
    def toggle_theme(current):
        new_theme = "light" if current == "dark" else "dark"
        css_class = "light-mode" if new_theme == "light" else "dark-mode"
        return new_theme, gr.update(elem_classes=css_class)

    toggle_btn.click(toggle_theme, inputs=theme_state, outputs=[theme_state, container])

demo.launch()
