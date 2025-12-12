package com.footballst.footballst.api.team.service;
import com.footballst.footballst.api.team.dto.TeamDashboardDto;

public interface TeamDashboardService {
    TeamDashboardDto getTeamDashboard(Long teamId, Integer season);
}
