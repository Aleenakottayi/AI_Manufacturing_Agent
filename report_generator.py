def generate_report(predicted_energy, carbon, suggestions):

    report = f"""
    Sustainability Report

    Predicted Energy Consumption: {predicted_energy:.2f} kWh
    Estimated Carbon Emission: {carbon:.2f} kg CO2

    Optimization Suggestions:
    """

    for s in suggestions:
        report += f"\n- {s}"

    return report