**Solving equations in numerical way.**

Examples:

1.  Solve x^2 + 2x + 3 = 0 with bisections method on interval (-5, 5) with precision eps. (Should find no roots)<br> `res = solve(lambda x: x * x + 2 * x + 3, -5, 5, eps, eps, 'bisections')`
2.  Solve x^2 + 2x + 3 = 0 with chords method on interval (-5, 5) with precision eps.<br> `res = solve(lambda x: x * x + 2 * x + 3, -5, 5, eps, eps, 'chords')`
2.  Solve x^2 + 2x + 3 = 0 with newton method on interval (-5, 5) with precision eps.<br> `res = solve(lambda x: x * x + 2 * x + 3, -5, 5, eps, eps, 'newton')`
3. More examples available at _\src\example\main.py_.

CLI:

`cli.py dat.data` where dat.data is path to .data file.
