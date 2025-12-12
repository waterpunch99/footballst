package com.footballst.footballst.api.team.service;

import com.footballst.footballst.api.team.TeamPerformance;
import com.footballst.footballst.api.team.TeamPerformanceRepository;
import com.footballst.footballst.api.team.TeamStats;
import com.footballst.footballst.api.team.TeamStatsRepository;
import com.footballst.footballst.api.team.dto.TeamDashboardDto;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class TeamDashboardServiceImpl implements TeamDashboardService {

    private final TeamStatsRepository teamStatsRepository;
    private final TeamPerformanceRepository teamPerformanceRepository;

    @Override
    public TeamDashboardDto getTeamDashboard(Long teamId, Integer season) {

        TeamStats stats = teamStatsRepository.findByIdTeamIdAndIdSeason(teamId, season)
                .orElseThrow(() -> new EntityNotFoundException("team_stats 없음"));

        TeamPerformance perf = teamPerformanceRepository.findByIdTeamIdAndIdSeason(teamId, season)
                .orElseThrow(() -> new EntityNotFoundException("team_performance 없음"));

        return TeamDashboardDto.builder()
                .teamId(teamId)
                .season(season)
                .summary(TeamDashboardDto.Summary.builder()
                        .totalMatches(stats.getTotalMatches())
                        .wins(stats.getWins())
                        .draws(stats.getDraws())
                        .losses(stats.getLosses())
                        .goalsFor(stats.getGoalsFor())
                        .goalsAgainst(stats.getGoalsAgainst())
                        .goalDiff(stats.getGoalDiff())
                        .winRate(stats.getWinRate())
                        .build()
                )
                .recent5(TeamDashboardDto.Recent5.builder()
                        .recent5WinRate(stats.getRecent5WinRate())
                        .recent5GoalDiff(stats.getRecent5GoalDiff())
                        .build()
                )
                .performance(TeamDashboardDto.Performance.builder()
                        .goalsPerMatch(perf.getGoalsPerMatch())
                        .goalsConcededPerMatch(perf.getGoalsConcededPerMatch())
                        .goalDiffPerMatch(perf.getGoalDiffPerMatch())
                        .build()
                )
                .build();
    }
}
