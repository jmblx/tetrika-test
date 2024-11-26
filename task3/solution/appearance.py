def merge_intervals(intervals, lesson_start, lesson_end):
    intervals = [(max(start, lesson_start), min(end, lesson_end)) for start, end in
                 zip(intervals[::2], intervals[1::2])]

    intervals = [interval for interval in intervals if interval[0] < interval[1]]

    intervals.sort()

    merged = []
    for current in intervals:
        if not merged or merged[-1][1] < current[0]:
            merged.append(current)
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], current[1]))
    return merged


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start, lesson_end = intervals['lesson']
    pupil_intervals = intervals['pupil']
    tutor_intervals = intervals['tutor']

    pupil_merged = merge_intervals(pupil_intervals, lesson_start, lesson_end)
    tutor_merged = merge_intervals(tutor_intervals, lesson_start, lesson_end)

    total_time = 0

    for p_start, p_end in pupil_merged:
        for t_start, t_end in tutor_merged:
            intersection_start = max(p_start, t_start)
            intersection_end = min(p_end, t_end)

            if intersection_start < intersection_end:
                intersection_duration = intersection_end - intersection_start
                total_time += intersection_duration
                print(f"Пересечение: Ученик ({p_start}, {p_end}) с Учителем ({t_start}, {t_end})")
                print(
                    f"Пересечение: с {intersection_start} по {intersection_end}, продолжительность: {intersection_duration} секунд")

    return total_time
