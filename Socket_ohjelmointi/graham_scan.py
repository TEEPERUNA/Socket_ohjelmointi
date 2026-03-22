import math
import os
import matplotlib.pyplot as plt

def read_points(filename):
    points = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(float, line.split())
                points.append((x, y))
    return points

def cross_product(O, A, B):
    """2D cross product of vectors OA and OB.
    Positive = counter-clockwise, negative = clockwise, 0 = collinear."""
    return (A[0] - O[0]) * (B[1] - O[1]) - (A[1] - O[1]) * (B[0] - O[0])

def graham_scan(points):
    points = list(set(points))  # remove duplicates
    n = len(points)
    if n < 3:
        return points

    # Step 1: Find the bottom-most point (lowest y, then leftmost x)
    pivot = min(points, key=lambda p: (p[1], p[0]))

    # Step 2: Sort by polar angle with respect to pivot
    def polar_angle_key(p):
        if p == pivot:
            return (-math.inf, 0)
        angle = math.atan2(p[1] - pivot[1], p[0] - pivot[0])
        dist = (p[0] - pivot[0])**2 + (p[1] - pivot[1])**2
        return (angle, -dist)  # for collinear: keep farthest

    sorted_pts = sorted(points, key=polar_angle_key)

    # Step 3: Graham scan
    stack = []
    for p in sorted_pts:
        while len(stack) >= 2 and cross_product(stack[-2], stack[-1], p) <= 0:
            stack.pop()
        stack.append(p)

    return stack

def main():
    # Look for graham.txt in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'graham.txt')

    pts = read_points(input_file)
    print(f"Total points: {len(pts)}")

    hull = graham_scan(pts)
    print(f"\nConvex Hull ({len(hull)} points):")
    for p in hull:
        print(f"  ({p[0]:.4f}, {p[1]:.4f})")

    # Close the hull for plotting
    hull_closed = hull + [hull[0]]
    hx = [p[0] for p in hull_closed]
    hy = [p[1] for p in hull_closed]

    # All points
    all_x = [p[0] for p in pts]
    all_y = [p[1] for p in pts]

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    for ax_plot, title, show_all in zip(axes,
                                        ['All Points + Convex Hull', 'Convex Hull Only'],
                                        [True, False]):
        if show_all:
            ax_plot.scatter(all_x, all_y, s=8, color='steelblue',
                            alpha=0.5, label=f'Points ({len(pts)})')
        ax_plot.plot(hx, hy, 'r-', linewidth=2, label='Convex Hull')
        ax_plot.scatter([p[0] for p in hull], [p[1] for p in hull],
                        s=60, color='red', zorder=5,
                        label=f'Hull vertices ({len(hull)})')
        ax_plot.set_title(title, fontsize=13, fontweight='bold')
        ax_plot.set_xlabel('X')
        ax_plot.set_ylabel('Y')
        ax_plot.legend()
        ax_plot.grid(True, alpha=0.3)
        ax_plot.set_aspect('equal')

    plt.suptitle('Graham Scan – Convex Hull', fontsize=15, fontweight='bold')
    plt.tight_layout()

    # Save plot next to the script
    output_path = os.path.join(script_dir, 'graham_scan.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nPlot saved to: {output_path}")
    plt.show()

if __name__ == '__main__':
    main()