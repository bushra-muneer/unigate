import { describe, expect, it } from 'vitest';

interface Group {
  id: string;
  name: string;
  tags: string[];
}

interface CourseWithGroups {
  courseId: string;
  courseName: string;
  groups: Group[];
}

function filterCoursesWithGroups(coursesWithGroups: CourseWithGroups[], searchQuery: string): CourseWithGroups[] {
  if (!searchQuery) return coursesWithGroups;
  const tokens = searchQuery.trim().toLowerCase().split(/\s+/);
  const multiple = tokens.length > 1;
  return coursesWithGroups
    .map((course) => {
      const filteredGroups = course.groups.filter((group) => {
        if (multiple) {
          return tokens.every((t) => group.tags?.some((tag) => tag.toLowerCase().includes(t)));
        }
        const query = tokens[0];
        return (
          group.name.toLowerCase().includes(query) ||
          course.courseName.toLowerCase().includes(query) ||
          group.tags?.some((tag) => tag.toLowerCase().includes(query))
        );
      });
      if (
        filteredGroups.length > 0 ||
        (!multiple && course.courseName.toLowerCase().includes(tokens[0]))
      ) {
        return {
          ...course,
          groups: filteredGroups,
        };
      }
      return null;
    })
    .filter((course): course is CourseWithGroups => course !== null);
}

describe('filterCoursesWithGroups', () => {
  const data: CourseWithGroups[] = [
    {
      courseId: '1',
      courseName: 'Capstone',
      groups: [
        { id: 'g1', name: 'Alpha', tags: ['project', 'ai'] },
        { id: 'g2', name: 'Beta', tags: ['blockchain'] },
      ],
    },
    {
      courseId: '2',
      courseName: 'Distributed Systems',
      groups: [
        { id: 'g3', name: 'Gamma', tags: ['network'] },
      ],
    },
  ];

  it('finds by partial group name', () => {
    const result = filterCoursesWithGroups(data, 'alp');
    expect(result.length).toBe(1);
    expect(result[0].groups[0].name).toBe('Alpha');
  });

  it('finds by partial course name', () => {
    const result = filterCoursesWithGroups(data, 'cap');
    expect(result.length).toBe(1);
    expect(result[0].courseName).toBe('Capstone');
  });

  it('finds by tag', () => {
    const result = filterCoursesWithGroups(data, 'block');
    expect(result.length).toBe(1);
    expect(result[0].groups[0].name).toBe('Beta');
  });

  it('is case-insensitive', () => {
    const result = filterCoursesWithGroups(data, 'CAPSTONE');
    expect(result.length).toBe(1);
    expect(result[0].courseName).toBe('Capstone');
  });

  it('returns empty for no match', () => {
    const result = filterCoursesWithGroups(data, 'nonexistent');
    expect(result.length).toBe(0);
  });
}); 