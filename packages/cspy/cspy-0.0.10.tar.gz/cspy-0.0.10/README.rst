cspy
====

A collection of algorithms for the (resource) Constrained Shortest Path
(CSP) problem.

The CSP problem was popularised by `Inrich 2005`_. 
It was initially introduced as a subproblem for the bus
driver scheduling problem, and has since then widely studied in a
variety of different settings including: the vehicle routing problem
with time windows (VRPTW), the technician routing and scheduling
problem, the capacitated arc-routing problem, on-demand transportation
systems, and, airport ground movement; among others.

More generally, in the applied column generation framework, particularly
in the scheduling related literature, the CSP problem is commonly
employed to generate columns.

Therefore, this library is of interest to the operational research
community, students and academics alike, that wish to solve an instance
of the CSP problem.

Algorithms
----------

Currently, the algorithms implemented include:

-  Monodirectional forward labeling algorithm;
-  Monodirectional backward labeling algorithm;
-  Bidirectional labeling algorithm with static halfway point;
-  Bidirectional labeling algorithm with dynamic halfway point `Tilk et al 2017`_;
-  Heuristic Tabu search;
-  Greedy elimination procedure;
-  Greedy Randomised Adaptive Search Procedure (GRASP). Adapted from
   `Ferone et al 2019`_;
- Particle Swarm Optimization with combined Local and Global Expanding Neighborhood Topology (PSOLGET) (`Marinakis et al 2017`_).

Features
--------

- Generic resource extension functions (`Inrich 2005`_) (not restricted to additive resources);
- Generic resource consumptions (not restricted to non-negative values).

Prerequisites
-------------

Conceptual background and input formatting is discussed in the
`docs`_.

Usage Examples
--------------

Please see the individual algorithms API Documentation for specific
examples and more details:

- ``BiDirectional``: `Bidirectional and monodirectional algorithms`_
- ``Tabu`` `Heuristic Tabu Search`_
- ``GreedyElim`` `Greedy Elimination Procedure`_
- ``GRASP`` `GRASP`_
- ``PSOLGENT`` `PSOLGENT`_ 


Please see individual algorithm documentation for examples.

.. _Bidirectional and monodirectional algorithms: https://cspy.readthedocs.io/en/latest/api/cspy.BiDirectional.html
.. _Heuristic Tabu Search: https://cspy.readthedocs.io/en/latest/api/cspy.Tabu.html
.. _Greedy Elimination Procedure: https://cspy.readthedocs.io/en/latest/api/cspy.GreedyElim.html
.. _Particle Swarm Optimization with combined Local and Global Expanding Neighborhood Topology: https://cspy.readthedocs.io/en/latest/api/cspy.PSOLGENT.html
.. _GRASP: https://cspy.readthedocs.io/en/latest/api/cspy.GRASP.html
.. _PSOLGENT: https://cspy.readthedocs.io/en/latest/api/cspy.PSOLGENT.html

Contributing
------------

Feel free to contribute to this project either by either working trough
some of issues flagged as help wanted, or raise a new issue with any
bugs/improvements.

If you have a question or need help, feel free to raise an
`issue`_ explaining it.


.. _Tilk et al 2017: https://www.sciencedirect.com/science/article/pii/S0377221717302035
.. _Inrich 2005: https://www.researchgate.net/publication/227142556_Shortest_Path_Problems_with_Resource_Constraints
.. _Marinakis et al 2017: https://www.sciencedirect.com/science/article/pii/S0377221717302357z
.. _Ferone et al 2019: https://www.tandfonline.com/doi/full/10.1080/10556788.2018.1548015
.. _docs: https://cspy.readthedocs.io/en/latest/how_to.html
.. _issue: https://github.com/torressa/cspy/issues
