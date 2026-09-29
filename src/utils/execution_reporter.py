"""
Execution Reporter module.

Provides a utility class to format and generate execution summaries
for the navigation algorithms.
"""


class ExecutionReporter:
    """
    Utility class responsible for generating and formatting the execution
    summary report of the map navigation processes.
    """

    @staticmethod
    def generate_report(
        width: int,
        height: int,
        obstacle_counts: dict[str, int],
        time_elapsed: float,
        path_stats: dict,
        is_test: bool = False,
        time_elapsed_rev: float = 0.0,
        reverse_stats: dict | None = None,
    ) -> str:
        """
        Generates a formatted string containing the execution summary.

        By returning a string rather than printing directly, this method
        allows the report to be printed to the console, saved to a file,
        or analyzed in automated tests.

        Args:
            width (int): The width of the grid.
            height (int): The height of the grid.
            obstacle_counts (dict[str, int]): The configuration of obstacles.
            time_elapsed (float): Execution time for the direct path.
            path_stats (dict): Statistics dictionary for the direct path.
            is_test (bool): Whether the reverse path test was executed. Defaults to False.
            time_elapsed_rev (float): Execution time for the reverse path. Defaults to 0.0.
            reverse_stats (dict | None): Statistics dictionary for the reverse path. Defaults to None.

        Returns:
            str: The fully formatted execution summary.
        """
        lines = []
        lines.append("\n" + "=" * 48)
        lines.append("                EXECUTION SUMMARY")
        lines.append("=" * 48)
        lines.append(f"Grid Dimensions   : {width}x{height}")

        total_obstacles = sum(obstacle_counts.values())
        lines.append(
            f"Grid Type         : {total_obstacles} obstacle elements configured"
        )

        lines.append("Obstacle Details  :")
        for obs_name, obs_count in obstacle_counts.items():
            lines.append(f"  - {obs_name:<11} : {obs_count}")
        lines.append("-" * 48)

        status_dir = "Interrupted" if path_stats.get("interrupted") else "Completed"
        lines.append(f"[Direct Path] ({status_dir})")
        lines.append(
            f"Total Valid Paths Evaluated     : {path_stats.get('paths_found', 0)}"
        )
        lines.append(
            f"Total Border Cells Found        : {path_stats.get('border_cells', 0)}"
        )
        lines.append(
            f"Condition (lF < len_min) = False: {path_stats.get('condition_false', 0)} times"
        )
        lines.append(f"Performance (Execution Time)    : {time_elapsed:.4f} seconds")

        if is_test and reverse_stats is not None:
            lines.append("-" * 48)
            status_rev = (
                "Interrupted" if reverse_stats.get("interrupted") else "Completed"
            )
            lines.append(f"[Reverse Path] ({status_rev})")
            lines.append(
                f"Total Valid Paths Evaluated     : {reverse_stats.get('paths_found', 0)}"
            )
            lines.append(
                f"Total Border Cells Found        : {reverse_stats.get('border_cells', 0)}"
            )
            lines.append(
                f"Condition (lF < len_min) = False: {reverse_stats.get('condition_false', 0)} times"
            )
            lines.append(
                f"Performance (Execution Time)    : {time_elapsed_rev:.4f} seconds"
            )

        lines.append("=" * 48 + "\n")

        # Uniamo tutte le linee con il carattere di a capo
        return "\n".join(lines)

    @classmethod
    def print_report(cls, *args, **kwargs) -> None:
        """
        Generates and immediately prints the execution report to the standard output.
        Accepts the same arguments as `generate_report`.
        """
        report = cls.generate_report(*args, **kwargs)
        print(report)
