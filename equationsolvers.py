#!/usr/bin/env python3
from sympy import Eq, latex, Function, exp, log, Abs, simplify

from sympy.parsing.sympy_parser import (parse_expr, convert_equals_signs,
    implicit_multiplication, standard_transformations,implicit_multiplication_application)
from textwrap import dedent

# Linear Equation Solver
def linear_solver(sub):
    r"""Linear Equation Checker/Solver.

    Checks whether a given string is a linear equation in one variable,
    and if so, returns an explanation of how to solve it.

    Parameters
    ----------

    sub : str
        The submitted expression, as a math string, to be passed to SymPy.

    Returns
    -------

    explanation:
        False if unable to parse as linear,
        A worked thorugh $\LaTeX$ explanation otherwise.

    Examples
    --------

    >>> linear_solver("")
    False

    >>> linear_solver("something abstract")
    False

    >>> linear_solver("x+1")
    False

    >>> linear_solver("x**2+1=1")
    False

    >>> print(linear_solver("x=1"))
    Let's solve the equation:
    \[
        x = 1
    \]
    The equation is in the form $x = 1$;
    That is, the value of $x$ is $1$.

    >>> print(linear_solver("x=0"))
    Let's solve the equation:
    \[
        x = 0
    \]
    The equation is in the form $x = 0$;
    That is, the value of $x$ is $0$.

    >>> print(linear_solver("a-1=1"))
    Let's solve the equation:
    \[
        a - 1 = 1
    \]
    First, we subtract -1 from both sides:
    \begin{align*}
        (a - 1)-(-1) &= 1-(-1) \\
        a &= 2
    \end{align*}
    The equation is in the form $a = 2$;
    That is, the value of $a$ is $2$.

    >>> print(linear_solver("5/3y=2"))
    Let's solve the equation:
    \[
        \frac{5 y}{3} = 2
    \]
    We have just one term on the left:
    The variable $y$ with coefficient $\frac{5}{3}$.
    Divide both sides by $\frac{5}{3}$:
    \begin{align*}
        \frac{ \frac{5 y}{3} }{ \frac{5}{3} } &=
        \frac{ 2 }{ \frac{5}{3} } \\
        y &= \frac{6}{5}
    \end{align*}
    The equation is in the form $y = \frac{6}{5}$;
    That is, the value of $y$ is $\frac{6}{5}$.

    >>> print(linear_solver("3a-1=1"))
    Let's solve the equation:
    \[
        3 a - 1 = 1
    \]
    First, we subtract -1 from both sides:
    \begin{align*}
        (3 a - 1)-(-1) &= 1-(-1) \\
        3 a &= 2
    \end{align*}
    We have just one term on the left:
    The variable $a$ with coefficient $3$.
    Divide both sides by $3$:
    \begin{align*}
        \frac{ 3 a }{ 3 } &=
        \frac{ 2 }{ 3 } \\
        a &= \frac{2}{3}
    \end{align*}
    The equation is in the form $a = \frac{2}{3}$;
    That is, the value of $a$ is $\frac{2}{3}$.

    >>> print(linear_solver("a-1=1"))
    Let's solve the equation:
    \[
        a - 1 = 1
    \]
    First, we subtract -1 from both sides:
    \begin{align*}
        (a - 1)-(-1) &= 1-(-1) \\
        a &= 2
    \end{align*}
    The equation is in the form $a = 2$;
    That is, the value of $a$ is $2$.
    """
    # Check if SymPy can parse the expression as an equation
    try:
        expr = parse_expr(sub,
                   transformations=(*standard_transformations,
                                    implicit_multiplication,
                                    convert_equals_signs))
    except (SyntaxError, ValueError):
        return False

    # Verify the structure of the equation

    # Check if the expression is in 1 variable
    variables = expr.free_symbols
    if len(variables) != 1:
        return False
    x, = variables

    # Check if it is a linear equation
    if not isinstance(expr, Eq):
        return False
    if not expr.rhs.is_constant():
        return False
    if not expr.lhs.diff(x).is_constant():
        return False

    # Now that we know the structure of the equation,
    # we can turn it into a worked-through solution.

    explanation = dedent("""\
    Let's solve the equation:
    \\[
        {expression}
    \\]
    """.format(expression=latex(expr)))
    lhs = expr.lhs
    rhs = expr.rhs
    coeff = lhs.coeff(x)
    left_constant = lhs - coeff*x

    # Use conditional blocks to construct content that only sometimes shows up.
    if not left_constant.is_zero:
        new_rhs = rhs - left_constant
        new_lhs = lhs - left_constant
        explanation += dedent("""\
        First, we subtract {left_constant} from both sides:
        \\begin{{align*}}
            ({old_lhs})-({left_constant}) &= {old_rhs}-({left_constant}) \\\\
            {new_lhs} &= {new_rhs}
        \\end{{align*}}
        """.format(left_constant = left_constant,
                   old_lhs = latex(lhs),
                   old_rhs = latex(rhs),
                   new_lhs = latex(new_lhs),
                   new_rhs = latex(new_rhs),
                   ))
        lhs = new_lhs
        rhs = new_rhs

    if not coeff == 1:
        new_rhs = rhs/coeff
        new_lhs = lhs/coeff
        explanation += dedent("""\
        We have just one term on the left:
        The variable ${variable}$ with coefficient ${coefficient}$.
        Divide both sides by ${coefficient}$:
        \\begin{{align*}}
            \\frac{{ {old_lhs} }}{{ {coefficient} }} &=
            \\frac{{ {old_rhs} }}{{ {coefficient} }} \\\\
            {new_lhs} &= {new_rhs}
        \\end{{align*}}
        """.format(coefficient = latex(coeff),
                   variable = latex(x),
                   old_lhs = latex(lhs),
                   old_rhs = latex(rhs),
                   new_lhs = latex(new_lhs),
                   new_rhs = latex(new_rhs),
                   ))
        lhs = new_lhs
        rhs = new_rhs

    explanation += dedent("""\
        The equation is in the form ${variable} = {value}$;
        That is, the value of ${variable}$ is ${value}$.""".format(
        variable = latex(x),
        value = latex(rhs)))

    return explanation


# Exponential
# Examples:
#     "e^x-5=2"
#     "1+2e^(x-1)=5"
#     "1-2e^(x-1)=5"
def exponential_solver(sub):
    return False


# Logarithm
# Examples:
#     "ln(x)=3"
#     "ln(2x)-1=4"
#     "ln(3x)+3=2"
#     "ln(3a+1)-1=3"
# As a challenge,
# You can also choose to support other formats of log
def logarithm_solver(sub):
    r"""
    Logarithmic Equation Checker/Solver.

    Checks whether a given string is a logarithmic equation in one variable,
    and if so, returns an explanation of how to solve it.

    Parameters
    ----------

    sub : str
        The submitted expression, as a math string, to be passed to SymPy.

    Returns
    -------

    explanation:
        False if unable to parse as logarithmic,
        A worked thorugh $\LaTeX$ explanation otherwise.

    Examples
    --------

    >>> logarithm_solver("")
    False

    >>> logarithm_solver("something abstract")
    False

    >>> logarithm_solver("x+1")
    False

    >>> logarithm_solver("x**2+1=1")
    False

    >>> print(logarithm_solver("ln(x)=3"))
    Let's solve the equation:
    \[
        \log{\left (x \right )} = 3
    \]
    we can kill the logarithm via exponentiation:
    \begin{align*}
        \exp{ (\log{\left (x \right )}) } &=
        \exp{ (3) } \\
        x &= e^{3}
    \end{align*}
    Let's solve the equation:
    \[
        x = e^{3}
    \]
    The equation is in the form $x = e^{3}$;
    That is, the value of $x$ is $e^{3}$.

    >>> print(logarithm_solver("ln(2x)-1=4"))
    Let's solve the equation:
    \[
        \log{\left (2 x \right )} - 1 = 4
    \]
    First, we subtract -1 from both sides:
    \begin{align*}
        (\log{\left (2 x \right )} - 1)-(-1) &= 4-(-1) \\
        \log{\left (2 x \right )} &= 5
    \end{align*}
    we can kill the logarithm via exponentiation:
    \begin{align*}
        \exp{ (\log{\left (2 x \right )}) } &=
        \exp{ (5) } \\
        2 x &= e^{5}
    \end{align*}
    Let's solve the equation:
    \[
        2 x = e^{5}
    \]
    We have just one term on the left:
    The variable $x$ with coefficient $2$.
    Divide both sides by $2$:
    \begin{align*}
        \frac{ 2 x }{ 2 } &=
        \frac{ e^{5} }{ 2 } \\
        x &= \frac{e^{5}}{2}
    \end{align*}
    The equation is in the form $x = \frac{e^{5}}{2}$;
    That is, the value of $x$ is $\frac{e^{5}}{2}$.

    >>> print(logarithm_solver("ln(3x)+3=2"))
    Let's solve the equation:
    \[
        \log{\left (3 x \right )} + 3 = 2
    \]
    First, we subtract 3 from both sides:
    \begin{align*}
        (\log{\left (3 x \right )} + 3)-(3) &= 2-(3) \\
        \log{\left (3 x \right )} &= -1
    \end{align*}
    we can kill the logarithm via exponentiation:
    \begin{align*}
        \exp{ (\log{\left (3 x \right )}) } &=
        \exp{ (-1) } \\
        3 x &= e^{-1}
    \end{align*}
    Let's solve the equation:
    \[
        3 x = e^{-1}
    \]
    We have just one term on the left:
    The variable $x$ with coefficient $3$.
    Divide both sides by $3$:
    \begin{align*}
        \frac{ 3 x }{ 3 } &=
        \frac{ e^{-1} }{ 3 } \\
        x &= \frac{1}{3 e}
    \end{align*}
    The equation is in the form $x = \frac{1}{3 e}$;
    That is, the value of $x$ is $\frac{1}{3 e}$.

    >>> print(logarithm_solver("ln(3a+1)-1=3"))
    Let's solve the equation:
    \[
        \log{\left (3 a + 1 \right )} - 1 = 3
    \]
    First, we subtract -1 from both sides:
    \begin{align*}
        (\log{\left (3 a + 1 \right )} - 1)-(-1) &= 3-(-1) \\
        \log{\left (3 a + 1 \right )} &= 4
    \end{align*}
    we can kill the logarithm via exponentiation:
    \begin{align*}
        \exp{ (\log{\left (3 a + 1 \right )}) } &=
        \exp{ (4) } \\
        3 a + 1 &= e^{4}
    \end{align*}
    Let's solve the equation:
    \[
        3 a + 1 = e^{4}
    \]
    First, we subtract 1 from both sides:
    \begin{align*}
        (3 a + 1)-(1) &= e^{4}-(1) \\
        3 a &= -1 + e^{4}
    \end{align*}
    We have just one term on the left:
    The variable $a$ with coefficient $3$.
    Divide both sides by $3$:
    \begin{align*}
        \frac{ 3 a }{ 3 } &=
        \frac{ -1 + e^{4} }{ 3 } \\
        a &= - \frac{1}{3} + \frac{e^{4}}{3}
    \end{align*}
    The equation is in the form $a = - \frac{1}{3} + \frac{e^{4}}{3}$;
    That is, the value of $a$ is $- \frac{1}{3} + \frac{e^{4}}{3}$.

    """
    # Check if SymPy can parse the expression as an equation
    try:
        expr = parse_expr(sub,
                   transformations=(*standard_transformations,
                                    implicit_multiplication,
                                    convert_equals_signs))
    except (SyntaxError, ValueError):
        return False

    # Verify the structure of the equation

    # Check if the expression is in 1 variable
    variables = expr.free_symbols
    if len(variables) != 1:
        return False
    x, = variables

    # Check if it is a logarithmic equation
    if not isinstance(expr, Eq):
        return False
    if not expr.rhs.is_constant():
        return False
    #theres probably a better way to do this.
    if not bool(expr.lhs.atoms(log)):#expr doesnt contains a logarithm
        return False
    elif !(lhs.atoms(sympy.log).pop().diff()*lhs.atoms(sympy.log).pop().args[0]).is_constant():
        return False

    # Now that we know the structure of the equation,
    # we can turn it into a worked-through solution.

    explanation = dedent("""\
    Let's solve the equation:
    \\[
        {expression}
    \\]
    """.format(expression=latex(expr)))
    lhs = expr.lhs
    rhs = expr.rhs

    left_constant = lhs.coeff(x,n=0)

    # Use conditional blocks to construct content that only sometimes shows up.
    if not left_constant.is_zero:
        new_rhs = rhs - left_constant
        new_lhs = lhs - left_constant
        explanation += dedent("""\
        First, we subtract {left_constant} from both sides:
        \\begin{{align*}}
            ({old_lhs})-({left_constant}) &= {old_rhs}-({left_constant}) \\\\
            {new_lhs} &= {new_rhs}
        \\end{{align*}}
        """.format(left_constant = left_constant,
                   old_lhs = latex(lhs),
                   old_rhs = latex(rhs),
                   new_lhs = latex(new_lhs),
                   new_rhs = latex(new_rhs),
                   ))
        lhs = new_lhs
        rhs = new_rhs

    # lhs should now be of the form c*log(ax+b) = rhs
    if len(lhs.args)!=1: #c≠1
        coeff = lhs.args[0]
        new_rhs = rhs/coeff
        new_lhs = lhs/coeff
        explanation += dedent("""\
        We have just one term on the left:
        The variable ${variable}$ with coefficient ${coefficient}$.
        Divide both sides by ${coefficient}$:
        \\begin{{align*}}
            \\frac{{ {old_lhs} }}{{ {coefficient} }} &=
            \\frac{{ {old_rhs} }}{{ {coefficient} }} \\\\
            {new_lhs} &= {new_rhs}
        \\end{{align*}}
        """.format(coefficient = latex(coeff),
                   variable = latex(x),
                   old_lhs = latex(lhs),
                   old_rhs = latex(rhs),
                   new_lhs = latex(new_lhs),
                   new_rhs = latex(new_rhs),
                   ))
        lhs = new_lhs
        rhs = new_rhs


    new_lhs = exp(lhs)
    new_rhs = exp(rhs)
    explanation += dedent("""\
        we can kill the logarithm via exponentiation:
        \\begin{{align*}}
            \\exp{{ ({lhs}) }} &=
            \\exp{{ ({rhs}) }} \\\\
            {new_lhs} &= {new_rhs}
        \\end{{align*}}
        """.format(lhs = latex(lhs),
                   rhs = latex(rhs),
                   new_lhs = latex(new_lhs),
                   new_rhs = latex(new_rhs),
                   ))
    lhs = new_lhs
    rhs = new_rhs

    return explanation+linear_solver(str(lhs)+"="+str(rhs))

# Square Roots
# Examples:
#     "sqrt(x+1)=2"
#     "2sqrt(2x-3)+3=5"
#     "1-2sqrt(2-x)=3"
# As a challenge, you can consider other roots like ^(1/3).
def square_root_solver(sub):
    return False


# Quadratic Equation Solver
# Examples:
#    "x**2+2x+1=0"
#    "y**2+1=0"
#    "z**2+3z+2=0"
def quadratic_solver(sub):
    # Check if SymPy can parse the expression as an equation
    try:
        expr = parse_expr(sub,
                   transformations=(*standard_transformations,implicit_multiplication,
                                    implicit_multiplication_application,
                                    convert_equals_signs))
    except (SyntaxError, ValueError):
        return False
    # Check if the expression is in 1 variable
    variables = expr.free_symbols
    if len(variables) != 1:
        return False
    x, = variables

    # Check if it is a quadratic equation
    if not isinstance(expr,Eq):
        return False
    if not expr.rhs.is_constant():
        return False
    if not expr.rhs == 0:
        return False
    if not expr.lhs.diff(x).diff(x).is_constant():
        return False
    if expr.lhs.diff(x).diff(x) == 0:
        return False
    explanation = dedent("""\
    Let's solve the equation:
    \\[
        {expression}
    \\]
    """.format(expression=latex(expr)))
    lhs = expr.lhs
    rhs = expr.rhs

    a_coeff = lhs.coeff(x,2)
    b_coeff = lhs.coeff(x,1)
    c_coeff = lhs.coeff(x,0)

    explanation += dedent("""\
    First we define the coefficients of the quadratic: a, b, c
    \\begin{{align*}}
        a = {a_coeff}\\\\
        b = {b_coeff}\\\\
        c = {c_coeff}\\\\
    \\end{{align*}}
    We can use these with the quadratic equation to solve for the roots!
    """.format(a_coeff = latex(a_coeff),b_coeff=latex(b_coeff),c_coeff=latex(c_coeff),))

    import math
    x1 = -b_coeff+math.sqrt(b_coeff**2-4*a_coeff*c_coeff)/(2*a_coeff)
    x2 = -b_coeff-math.sqrt(b_coeff**2-4*a_coeff*c_coeff)/(2*a_coeff)
    explanation += dedent("""\
    The roots of this quadratic equation are ${x1}$ and ${x2}$.""".format(
    x1 = latex(x1),
    x2 = latex(x2)
    ))

    return explanation
# Systems of Linear Equations Solver
# Examples:
#     "a+2b = 1,a-b=3"
#     "3x+2/3y=5/2,5x-y=2"
# You can do it in only two dimensions if you want,
# or challenge yourself to do it for more.
def system_of_linear_equations_solver(sub):
    return False


# Export solvers as a list
equation_solvers = (linear_solver,
                    quadratic_solver,
                    logarithm_solver,
                    exponential_solver,
                    square_root_solver,
                    system_of_linear_equations_solver,
                    )


if __name__ == "__main__":
    import doctest
    doctest.testmod()
