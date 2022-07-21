from unittest import TestCase
from main import Tree
import pandas as pd


class TestTree(TestCase):
    df1 = pd.read_excel(r'data1.xlsx')
    df2 = pd.read_excel(r'data2.xlsx')

    # Тесты работают если запускать их по отдельности
    def test1(self):
        tree1 = Tree(self.df1, 'класс1', 'класс2')
        self.assertEqual(tree1.get_children(), ['a', 'd', 'c', 'b'])

    def test2(self):
        tree2 = Tree(self.df1, 'класс1', 'класс2')
        self.assertEqual(tree2.get_children(('класс1', '11')), ['a', 'd', 'c'])

    def test3(self):
        tree = Tree(self.df1, 'класс1', 'класс2')
        self.assertEqual(tree.get_children(('класс1', '11'), ('класс2', '21')), ['a', 'd'])

    def test4(self):
        tree = Tree(self.df2, 'класс1', 'класс2', 'класс3')
        self.assertEqual(tree.get_children(('класс2', '22')), ['d'])

    def test5(self):
        tree = Tree(self.df2, 'класс1', 'класс2', 'класс3')
        self.assertEqual(tree.get_children(('класс3', '22')), ['a', 'b'])

    def test6(self):
        tree = Tree(self.df2, 'класс1', 'класс3')
        self.assertEqual(tree.get_children(('класс3', '11')), ['e'])
