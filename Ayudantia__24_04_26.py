import math

class FailurePlane:
    def __init__(self, beta, cohesion, phi):
        """
        Representa el plano de falla.

        Parámetros:
            beta     : Ángulo de buzamiento del plano de falla (grados).
            cohesion : Cohesión del plano (kPa).
            phi      : Ángulo de fricción interna del plano (grados).
        """
        self.beta = beta
        self.cohesion = cohesion
        self.phi = phi
        self.beta_rad = math.radians(beta)
        self.phi_rad = math.radians(phi)

    def show(self):
        """Retorna un string con las propiedades del plano de falla."""
        return (
            f"  Angulo (beta)          : {self.beta:.2f} grados\n"
            f"  Cohesion (c)           : {self.cohesion:.2f} kPa\n"
            f"  Angulo de friccion (phi): {self.phi:.2f} grados"
        )


class SlopeAnalysis:
    def __init__(self, plane, H, alpha, gamma):
        """
        Analiza la estabilidad de un talud con mecanismo de falla plana.

        Se asume bloque triangular 2D con ancho unitario (1 m),
        talud recto y cresta horizontal. El criterio de rotura es
        Mohr-Coulomb (cohesión + fricción).

        Parámetros:
            plane : Objeto FailurePlane con propiedades de la discontinuidad.
            H     : Altura vertical del talud (m).
            alpha : Ángulo de la cara del talud medido desde la horizontal (grados).
            gamma : Peso unitario de la roca (kN/m³).

        Restricción geométrica:
            alpha > beta : condición necesaria para que exista bloque deslizante.
        """
        self.plane = plane
        self.H = H
        self.alpha = alpha
        self.gamma = gamma

        if alpha <= plane.beta:
            raise ValueError(
                f"Ángulo del talud (alpha={alpha}) debe ser mayor que "
                f"el ángulo de buzamiento (beta={plane.beta}) para que ocurra el deslizamiento."
            )

    def block_weight(self):
        """
        Calcula el peso del bloque deslizante por metro de ancho.

        Fórmula para bloque triangular con cresta horizontal:
            W = γ · (H² / 2) · (cot β − cot α)

        Retorna:
            W : Peso del bloque (kN/m).
        """
        cot_beta  = 1 / math.tan(self.plane.beta_rad)
        cot_alpha = 1 / math.tan(math.radians(self.alpha))
        volume = (self.H ** 2 / 2) * (cot_beta - cot_alpha)
        return self.gamma * volume

    def failure_area(self):
        """
        Calcula el área de la superficie de falla por metro de ancho.

        Para geometría general (cresta horizontal, cara recta):
            A = H · sin(α − β) / [sin(α) · sin(β)]

        Esta expresión proviene de la ley de senos aplicada al triángulo
        formado por la cara del talud, el plano de falla y la horizontal.

        Retorna:
            A : Área de falla (m²/m).
        """
        alpha_rad = math.radians(self.alpha)
        beta_rad  = self.plane.beta_rad
        return self.H * math.sin(alpha_rad - beta_rad) / (math.sin(alpha_rad) * math.sin(beta_rad))

    def factor_of_safety(self):
        """
        Calcula el Factor de Seguridad (FS) para falla plana sin agua.

        Criterio Mohr-Coulomb:
            FS = [c·A + W·cos(β)·tan(φ)] / [W·sin(β)]

        Donde:
            c·A      : componente cohesiva de la resistencia
            W·cos(β) : fuerza normal sobre el plano de falla
            W·sin(β) : fuerza motriz (componente tangencial del peso)

        Retorna:
            FS : Factor de seguridad.
        """
        A = self.failure_area()
        W = self.block_weight()

        resisting = (self.plane.cohesion * A) + (W * math.cos(self.plane.beta_rad) * math.tan(self.plane.phi_rad))
        driving   = W * math.sin(self.plane.beta_rad)

        if driving == 0:
            raise ZeroDivisionError("La fuerza motriz es cero. Verifique el ángulo de buzamiento.")

        return resisting / driving

    def report(self):
        """
        Imprime el reporte completo del análisis de estabilidad.

        Retorna:
            FS : Factor de seguridad calculado.
        """
        W  = self.block_weight()
        A  = self.failure_area()
        FS = self.factor_of_safety()

        if FS < 1.0:
            status = "INESTABLE (FS < 1.0)"
        elif FS < 1.3:
            status = "CRITICO (1.0 <= FS < 1.3)"
        else:
            status = "ESTABLE (FS >= 1.3)"

        print(
            f"\n{'='*50}\n"
            f"        ANALISIS DE ESTABILIDAD\n"
            f"{'='*50}\n"
            f"  Altura talud (H)        : {self.H:.2f} m\n"
            f"  Angulo del talud (alpha): {self.alpha:.2f} grados\n"
            f"  Peso unitario (gamma)   : {self.gamma:.2f} kN/m3\n"
            f"{'-'*50}\n"
            f"{self.plane.show()}\n"
            f"{'-'*50}\n"
            f"  Area de falla (A)       : {A:.2f} m2\n"
            f"  Peso del bloque (W)     : {W:.2f} kN\n"
            f"  Factor de Seguridad (FS): {FS:.4f}\n"
            f"{'='*50}\n"
            f"  ESTATUS: {status}\n"
            f"{'='*50}\n"
        )
        return FS


# DESAFIO DE TRABAJO PERSONAL

def find_critical_plane():
    """
    Evalúa 5 escenarios con distintos ángulos e identifica
    el plano más crítico (menor FS). Los demás parámetros del talud se
    mantienen constantes en todos los escenarios.
    """
    H     = 12.0
    alpha = 70.0
    gamma = 26.0

    scenarios = [
        (30.0, 40.0, 25.0),
        (35.0, 40.0, 25.0),
        (40.0, 40.0, 25.0),
        (45.0, 40.0, 25.0),
        (50.0, 40.0, 25.0),
    ]

    valid_analyses = []
    for beta, c, phi in scenarios:
        plane = FailurePlane(beta=beta, cohesion=c, phi=phi)
        try:
            valid_analyses.append(SlopeAnalysis(plane=plane, H=H, alpha=alpha, gamma=gamma))
        except ValueError as e:
            print(f"Escenario beta={beta} omitido: {e}")

    if not valid_analyses:
        print("No se encontraron escenarios validos. Verifique los angulos.")
        return

    fs_values = [a.factor_of_safety() for a in valid_analyses]
    min_fs    = min(fs_values)
    critical  = valid_analyses[fs_values.index(min_fs)]

    tabla = "\n".join(
        f"  {i+1:<10} {a.plane.beta:<12.1f} {fs:<10.4f} {'CRITICO' if fs == min_fs else ''}"
        for i, (a, fs) in enumerate(zip(valid_analyses, fs_values))
    )

    print(
        f"\n{'-'*55}\n"
        f"{'DESAFIO: ENCONTRANDO EL PLANO DE FALLA CRITICO':^55}\n"
        f"{'-'*55}\n\n"
        f"  {'Escenario':<10} {'beta (deg)':<12} {'FS':<10} {'Nota'}\n"
        f"  {'-'*43}\n"
        f"{tabla}\n\n"
        f"  Plano critico: beta = {critical.plane.beta} grados  |  FS minimo = {min_fs:.4f}\n"
    )

    critical.report()
    return critical


if __name__ == "__main__":
    print("EJERCICIO 1")
    plane1 = FailurePlane(beta=35, cohesion=50, phi=30)
    print(plane1.show())

    print("\nEJERCICIO 2")
    analysis1 = SlopeAnalysis(
        plane=FailurePlane(beta=35, cohesion=50, phi=30),
        H=10,
        alpha=60,
        gamma=25
    )
    analysis1.report()

    find_critical_plane()