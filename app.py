from flask import Flask, render_template, request
import sympy as sp
import re


app = Flask(__name__)

x = sp.symbols('x')


def calculate_derivative(expression):
    derivative = sp.diff(expression, x)
    print("the derivative is ", derivative)
    return derivative


def calculate_integral(expression):
    integral = sp.integrate(expression, x)
    print("the integral is ", integral)
    return integral


def solve_equation(equation):
    solutions = sp.solve(equation, x)
    return solutions


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/calculus', methods=['GET', 'POST'])
def calculus():
    result = None
    latex_result = None
    error = None

    if request.method == 'POST':

        expression_str = request.form['mathquill_plain']
        data_type = type(expression_str)
        print("Data type of expression_str:", data_type)

        print("the string field is ", expression_str)
        operation = request.form['operation']

        cleaned_str = clean_and_sympify(expression_str)

        try:
            print("the expression before is ", cleaned_str)
            # expression = sp.sympify(cleaned_string)
            # print("the expression after is ", expression)

            if operation == 'derivative':
                result = calculate_derivative(cleaned_str)
                latex_result = sp.latex(result)
                print("Derivative Result:", latex_result)
            elif operation == 'integral':
                result = calculate_integral(cleaned_str)
                print("Integral Result:", latex_result)
                latex_result = sp.latex(result)

        except (sp.SympifyError, ValueError):
            error = "Invalid input. Please enter a valid mathematical expression."

    return render_template('calculus.html', error=error, latex_result=latex_result)


@app.route('/equation_solver', methods=['GET', 'POST'])
def equation_solver():
    solutions = None
    latex_solutions = None
    error = None

    if request.method == 'POST':
        equation_str = request.form['mathquill_plain']
        # Find the position of the equal sign
        equal_sign_index = equation_str.find('=')

        # if index array with '=' found
        if equal_sign_index != -1:
            # Remove characters from equal sign onwards
            equation_str = equation_str[:equal_sign_index]

        try:
            cleaned_str = clean_and_sympify(equation_str)
            equation = sp.sympify(cleaned_str)
            solutions = solve_equation(equation)
            latex_solutions = sp.latex(solutions)
            print("The solution is ", latex_solutions)
        except (sp.SympifyError, ValueError):
            solutions = "Invalid input. Please enter a valid equation."

    return render_template('equation_solver.html', error=error, latex_solutions=latex_solutions)


def clean_and_sympify(expression_str):
  # Replace asterisks (*) with the multiplication symbol (·)

    replacements = {
        r'\s*i*n *(': 'sin(',
        r'\c*o*s *(': 'cos(',
        r'\t*a*n *(': 'tan(',
        r'\l*o*g *(': 'log(',
    }

    # Iterate through the dictionary and apply replacements
    for pattern, replacement in replacements.items():
        expression_str = expression_str.replace(pattern, replacement)

    print("the cleaned string is ", expression_str)
    try:
        expression = sp.sympify(expression_str)
        return expression
    except Exception as e:
        return None


if __name__ == "__main__":
    app.run(debug=True)
