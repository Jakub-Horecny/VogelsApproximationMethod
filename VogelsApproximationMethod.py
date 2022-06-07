import sys
from typing import List


class VogelsApproximationMethod:
    """
    Vogel's Approximation Method (VAM) is one of the methods used to calculate
    the initial basic feasible solution to a transportation problem.
    """

    def __init__(self):
        self.supply = None
        self.demand = None
        self.costs = None  # matrix

        self.n_rows = None
        self.n_cols = None

        self.row_done = None
        self.col_done = None

        # na zobrazenie
        self.from_where = None
        self.where = None
        self.how_much = None

    def __reset(self):
        self.supply: list = []
        self.demand: list = []
        self.costs: list = []  # matrix

        self.n_rows: int = 0
        self.n_cols: int = 0

        self.row_done: list = []
        self.col_done: list = []

        # na zobrazenie
        self.from_where: list = []
        self.where: list = []
        self.how_much: list = []

    def __max_penalty_row(self) -> list:
        """
        finds max penalty in row
        :return: column index, row index, min price, max penalty
        :rtype list
        """
        row_index: int = -sys.maxsize - 1  # row index
        col_index: int = -sys.maxsize - 1  # column index
        min_cost: int = -sys.maxsize - 1  # lowest price
        max_diff: int = -sys.maxsize - 1  # penalty
        penalty: List[int]
        for i in range(self.n_rows):
            if self.row_done[i]:
                continue
            penalty = self.__diff_row(i)
            if penalty[0] > max_diff:
                max_diff = penalty[0]
                col_index = i
                min_cost = penalty[1]
                row_index = penalty[2]

        return [col_index, row_index, min_cost, max_diff]

    def __max_penalty_col(self) -> list:
        """
        finds max penalty in column
        :return: column index, row index, min price, max penalty
        :rtype list
        """
        row_index: int = -sys.maxsize - 1  # row index
        col_index: int = -sys.maxsize - 1  # column index
        min_cost: int = -sys.maxsize - 1  # lowest price
        max_diff: int = -sys.maxsize - 1  # penalty
        penalty: List[int]
        for i in range(self.n_cols):
            if self.col_done[i]:
                continue
            penalty = self.__diff_col(i)
            if penalty[0] > max_diff:
                max_diff = penalty[0]
                col_index = i
                min_cost = penalty[1]
                row_index = penalty[2]
        return [row_index, col_index, min_cost, max_diff]

    def __diff_col(self, j) -> list:
        """
        finds two lowest prices in column
        :param j: column index
        :return: difference between two lowest prices, the lowest price, index of the lowest price
        :rtype: list
        """
        min_penalty1: int = sys.maxsize  # min price
        min_penalty2: int = sys.maxsize  # second lowest price
        min_penalty_index: int = sys.maxsize # index of the lowest price
        cost: int
        for i in range(self.n_rows):
            if self.row_done[i]:
                continue
            cost = self.costs[i][j]
            if cost < min_penalty1:
                min_penalty2 = min_penalty1
                min_penalty1 = cost
                min_penalty_index = i
            elif cost < min_penalty2:
                min_penalty2 = cost
        return [min_penalty2 - min_penalty1, min_penalty1, min_penalty_index]

    def __diff_row(self, j):
        """
        finds two lowest prices in row
        :param j: row index
        :return: difference between two lowest prices, the lowest price, index of the lowest price
        """
        min_penalty1: int = sys.maxsize
        min_penalty2: int = sys.maxsize
        min_penalty_index: int = sys.maxsize
        cost: int
        for i in range(self.n_cols):
            if self.col_done[i]:
                continue
            cost = self.costs[j][i]
            if cost < min_penalty1:
                min_penalty2 = min_penalty1
                min_penalty1 = cost
                min_penalty_index = i
            elif cost < min_penalty2:
                min_penalty2 = cost
        return [min_penalty2 - min_penalty1, min_penalty1, min_penalty_index]

    def __next_cell(self) -> list:
        """
        finds row or column with the lowest price
        :return: indexes of the lowest price, value of the lowest price, max penalty
        """
        res1: list = self.__max_penalty_row()
        res2: list = self.__max_penalty_col()

        if res1[3] < res2[3]:
            if res1[2] < res2[2]:
                return res1
            else:
                return res2
        if self.n_rows > self.n_cols:
            if res1[3] > res2[3]:
                return res2
            else:
                return res1
        else:
            if res1[3] < res2[3]:
                return res2
            else:
                return res1

    def start(self, supply: list, demand: list, costs: list):
        """
        starts Vogel's Approximation Method
        :param supply: supply
        :param demand: demand
        :param costs: distance matrix
        :return: total cost
        """
        self.__reset()

        self.supply = supply
        self.demand = demand
        self.costs = costs

        self.n_rows = len(self.supply)
        self.n_cols = len(self.demand)

        self.row_done = [False] * self.n_rows
        self.col_done = [False] * self.n_cols

        supply_left = sum(self.supply)
        demand_left = sum(self.demand)
        total_cost = 0

        while supply_left > 0 and demand_left > 0:
            cell = self.__next_cell()
            r = cell[0]  # odkial
            self.from_where.append(r)
            c = cell[1]  # kam
            self.where.append(c)
            quantity = min(self.demand[c], self.supply[r])  # kolko
            self.how_much.append(quantity)

            self.demand[c] -= quantity
            if self.demand[c] == 0:
                self.col_done[c] = True

            self.supply[r] -= quantity
            if self.supply[r] == 0:
                self.row_done[r] = True

            supply_left -= quantity
            demand_left -= quantity
            total_cost += quantity * self.costs[r][c]

        return total_cost
