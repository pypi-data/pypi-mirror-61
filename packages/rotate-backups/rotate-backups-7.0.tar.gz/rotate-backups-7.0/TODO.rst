Feedback van Bart na pl-mysql-backup integratie:

- Validatie op invalid keys (months versus monthly mag best een exception raisen).
- Coercion van retention periods binnen de Python API zodat callers dit niet hoeven te doen.
