
def optimize(temperature, time, output, predicted_energy):

    suggestions = []

    if predicted_energy > 250:
        suggestions.append("Reduce machine speed to lower energy usage.")

    if temperature > 80:
        suggestions.append("Adjust cooling system to reduce overheating.")

    if time > 10:
        suggestions.append("Optimize batch scheduling.")

    if not suggestions:
        suggestions.append("System operating efficiently.")

    return suggestions