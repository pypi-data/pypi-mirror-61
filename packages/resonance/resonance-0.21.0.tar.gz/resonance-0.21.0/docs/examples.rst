========
Examples
========

Single Degree of Freedom Linear System
======================================

The linear equations for a compound pendulum with an external torque applied at
its pivot are as follows:

.. math::

   (I + ml^2) \ddot(\theta) + mgl\theta = T

::

   >>> from resonance.linear_systems import SingleDoFLinearSystem
   >>> pendulum = SingleDoFLinearSystem()

The first step is to declare the name and corresponding value to the constants
(non-time varying parameters) in the system.

::

   >>> pendulum.constants['I'] = 0.5  # kg*m**2
   >>> pendulum.constants['m'] = 1.2  # kg
   >>> pendulum.constants['g'] = 9.8  # m/s**2
   >>> pendulum.constants['l'] = 0.3  # m

Now specify the coordinates and speeds (time derivatives of the coordinates)::

   >>> pendulum.coordinates['theta'] = 0.0  # rad
   >>> pendulum.speeds['thetadot'] = 0.0  # rad/s

The last step in fully defining the system is to specify the equations of
motion. For a single degree of freedom system, only the mass, damping, and
stiffness coefficients need to be specified based on this canonical form:

.. math::

   m \ddot{x} + c \dot{x} + k x = f

To do this, create a function that returns m, c, k::

   >>> def calc_coeffs(I, m, l, g):
   ...     m = I + m*l**2
   ...     c = 0.0
   ...     k = m*g*l
   ...     return m, c, k
   ...

Now make the system aware of this function::

   >>>:
