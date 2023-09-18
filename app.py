from flask import Flask, render_template, request
import sympy as sp

app = Flask(__name__)

x = sp.symbols('x')


def calculate_derivative(expression):
    derivative = sp.diff(expression, x)
    return derivative


def calculate_integral(expression):
    integral = sp.integrate(expression, x)
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
        expression_str = request.form['expression']
        operation = request.form['operation']

        try:
            expression = sp.sympify(expression_str)

            if operation == 'derivative':
                result = calculate_derivative(expression)
                latex_result = sp.latex(result)
                print("Derivative Result:", latex_result)
            elif operation == 'integral':
                result = calculate_integral(expression)
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
        equation_str = request.form['equation']
        # Find the position of the equal sign
        equal_sign_index = equation_str.find('=')

        # if index array with '=' found
        if equal_sign_index != -1:
            # Remove characters from equal sign onwards
            equation_str = equation_str[:equal_sign_index]

        try:
            equation = sp.sympify(equation_str)
            solutions = solve_equation(equation)
            latex_solutions = sp.latex(solutions)
            print("The solution is ", latex_solutions)
        except (sp.SympifyError, ValueError):
            solutions = "Invalid input. Please enter a valid equation."

    return render_template('equation_solver.html', error=error, latex_solutions=latex_solutions)


if __name__ == "__main__":
    app.run(debug=True)
