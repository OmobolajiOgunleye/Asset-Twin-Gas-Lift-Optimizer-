Asset-Twin:Gas Lift Optimizer
An algorithmic digital twin built with Python and Streamlit using non-linear math optimization to resolve gas-lift allocation bottlenecks under constrained asset parameters.

The Problem
Imagine a manufacturing plant with five automated production lines. To keep products flowing, all five lines share a single, central air compressor. 

Here is the bottleneck:
1) Different Efficiencies: Every line responds differently. Giving 50 units of air pressure to Line 1 might double its speed, but giving it to Line 2 might cause it to choke and slow down due to friction.
2) Strict Constraints: The main compressor has a hard limit—it can only output 300 units of pressure in total. 

Traditionally, floor operators use slow, manual guesswork to split the pressure. This leads to massive energy waste, missed production targets, and mechanical wear on the valves.

What This Digital Twin Does
This Asset Twin acts as an algorithmic decision-making brain. Instead of a human guessing the distribution, this software uses advanced mathematical optimization to find the "exact magic combination" that squeezes the absolute maximum output from all 5 lines simultaneously without breaking the compressor limit.

In heavy industries (like the upstream oil and gas assets where I work), this technique is applied to gas-lift wells. However, the underlying mathematics map perfectly to Fast-Moving Consumer Goods (FMCG) plants, chemical blending loops, and automated bottling lines.

Research & Manufacturing Architecture
This project serves as a functional prototype bridging Data Analytics and Industrial Automation within the framework of Industry 4.0 pillars:

- Smart & Digital Technologies:Translating manual production engineering monitoring into a responsive, real-time web interface.
- Resource Sustainability (Clean Tech):Optimizing compressor loads directly reduces secondary power consumption, lowering the facility's carbon footprint.
- Predictive Asset Integrity:Restricting optimization limits prevents turbulent over-injection shocks, extending the lifespans of downhole valves and manifold hardware.

The Optimization Logic
The backend uses an industry-standard math engine called the "Sequential Least Squares Programming (SLSQP)" algorithm. Each production line is modeled using physics-based equations that track actual fluid behavior. 

The program dynamically calculates two things simultaneously:

1) The Primary Goal (Maximize Output): It analyzes how every individual line responds to pressure and continuously re-allocates resources to achieve the absolute highest total output possible for the entire plant.
2) The Golden Rule (The System Limit): It sets a strict mathematical boundary ensuring that the combined resource assigned to Line 1 + Line 2 + Line 3 + Line 4 + Line 5 will never exceed your maximum Compressor Limit.


Technical Stack
Algorithmic Engine:Python, NumPy, SciPy (Optimization Module)
Interactive Frontend:Streamlit Framework
Data Visualization:Plotly Engine
