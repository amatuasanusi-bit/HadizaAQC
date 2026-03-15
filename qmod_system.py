from core.graph_model import InfrastructureGraph
from core.energy_model import EnergyModel
from intelligence.prediction_engine import PredictionEngine
from intelligence.qgad_detector import QGAD
from intelligence.risk_resilience import RiskAnalyzer
from optimization.qubo_builder import QUBOBuilder
from optimization.classical_solver import ClassicalAnnealer

class QMOD:

    def __init__(self):

        self.graph = InfrastructureGraph()
        self.energy = EnergyModel()
        self.predictor = PredictionEngine()
        self.qgad = QGAD()
        self.risk = RiskAnalyzer()
        self.qubo = QUBOBuilder()
        self.solver = ClassicalAnnealer()

    def optimize(self):

        energy, nodes = self.energy.build_energy_matrix(self.graph)

        Q = self.qubo.build(energy)

        solution, energy_val = self.solver.solve(Q)

        return solution, energy_val, nodes