package com.footballst.footballst.api.team.controller;

import com.footballst.footballst.api.team.dto.TeamDashboardDto;
import com.footballst.footballst.api.team.service.TeamDashboardService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/teams")
public class TeamDashboardController {

    private final TeamDashboardService teamDashboardService;

    @GetMapping("/{teamId}/dashboard")
    public ResponseEntity<TeamDashboardDto> getDashboard(
            @PathVariable Long teamId,
            @RequestParam(defaultValue = "2023") Integer season
    ) {
        return ResponseEntity.ok(
                teamDashboardService.getTeamDashboard(teamId, season)
        );
    }
}
