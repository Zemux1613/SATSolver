from nltk.sem import logic

# Ensure the logic parser uses the standard first-order logic symbols
logic._counter._value = 0

# Define logical constants TRUE and FALSE
TRUE = logic.Expression.fromstring('1')
FALSE = logic.Expression.fromstring('0')


class DNFSolver():

    def simplify_formula(self, formula):
        """
        Apply simplification laws recursively to the given logical formula.

        :param formula: The logical formula in string format
        :return: The simplified formula
        """
        parsed_formula = logic.Expression.fromstring(formula)

        def apply_laws(expression):
            if isinstance(expression, logic.OrExpression):
                first_simplified = apply_laws(expression.first)
                second_simplified = apply_laws(expression.second)

                if first_simplified == second_simplified:
                    # x or x = x
                    return first_simplified
                elif first_simplified == TRUE or second_simplified == TRUE:
                    # x or 1 = 1
                    return TRUE
                elif first_simplified == FALSE:
                    # x or 0 = x
                    return second_simplified
                elif second_simplified == FALSE:
                    # 0 or x = x
                    return first_simplified
                else:
                    return logic.OrExpression(first_simplified, second_simplified)

            elif isinstance(expression, logic.AndExpression):
                first_simplified = apply_laws(expression.first)
                second_simplified = apply_laws(expression.second)

                if first_simplified == second_simplified:
                    # x and x = x
                    return first_simplified
                elif first_simplified == TRUE:
                    # 1 and x = x
                    return second_simplified
                elif second_simplified == TRUE:
                    # x and 1 = x
                    return first_simplified
                elif first_simplified == FALSE or second_simplified == FALSE:
                    # x and 0 = 0
                    return FALSE
                else:
                    return logic.AndExpression(first_simplified, second_simplified)

            elif isinstance(expression, logic.NegatedExpression):
                term_simplified = apply_laws(expression.term)

                if isinstance(term_simplified, logic.NegatedExpression):
                    # --x = x
                    return apply_laws(term_simplified.term)
                else:
                    return logic.NegatedExpression(term_simplified)

            else:
                return expression

        simplified_formula = apply_laws(parsed_formula)

        # Check if further simplification is possible
        if str(simplified_formula) != str(parsed_formula):
            return self.simplify_formula(str(simplified_formula))
        else:
            return str(simplified_formula)

    def solve_monom(self, monom):
        '''
        Solve single monom, in O(n^2)
        :param monom: formula to be solved
        :return: is satisfied or not
        '''
        # 1 Literal in Monom
        if "&" not in monom:
            return True

        # Literale > 1 im Monom
        literals = []
        for literal in monom.replace("(", "").replace(")", "").split("&"):
            literals.append(literal.strip())

        # check literal with negat in monom
        for literal1 in literals:
            for literal2 in literals:
                if "-" + literal1 == literal2 or "'" + literal2 == literal1:
                    return False
        print(f"Monom: {monom}\nLiterals: {literals}\n")
        return True

    def solve(self, formula):
        '''
        algorithm is in O(n^3)
        :param monom: formula to be solved
        :return: is satisfied or not
        '''
        # DNF mit > 1 Monom
        if "|" in formula:
            monoms = [monom for monom in str('(' + formula.strip("()") + ')').split("|")]
            for monom in monoms:
                return self.solve_monom(monom)
        # DNF mit 1 Monom
        else:
            return self.solve_monom(formula)
