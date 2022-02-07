import unittest
from convert_math import convert
import os

class TestDumpConvert(unittest.TestCase):

    def setUp(self) -> None:
        self.tex_path = 'math_expression.tex'
        if not os.path.exists(self.tex_path):
            with open(self.tex_path, 'w') as f:
                f.write("\\documentclass{article}\n" +
                        "\\usepackage{amsmath}\n" +
                        "\\begin{document}\n" +
                        "$$ $$\n" +
                        "\\end{document}")

    def test_convert_Albedo(self):
        with open("test/Albedo.txt", "r") as t:
            with open("test/Albedo.html", "r") as h:
                result_Albedo = convert(t.read().replace("\n", ""), self.tex_path)[0]
                self.assertEqual(result_Albedo, h.read().replace("\n", ""))

    def test_convert_Ampere(self):
        with open("test/Ampere.txt", "r") as t:
            with open("test/Ampere.html", "r") as h:
                result_Ampere = convert(t.read().replace("\n", ""), self.tex_path)[0]
                self.assertEqual(result_Ampere, h.read().replace("\n", ""))

    def test_convert_Arithmetic_mean(self):
        with open("test/Arithmetic_mean.txt", "r") as t:
            with open("test/Arithmetic_mean.html", "r") as h:
                result_Arithmetic_mean = convert(t.read().replace("\n", ""), self.tex_path)[0]
                self.assertEqual(result_Arithmetic_mean, h.read().replace("\n", ""))

    def tearDown(self) -> None:
        if os.path.exists(self.tex_path):
            os.remove(self.tex_path)
        if os.path.exists("combined.html"):
            os.remove("combined.html")
        if os.path.exists("actual.tex"):
            os.remove("actual.tex")


if __name__ == '__main__':
    unittest.main()
