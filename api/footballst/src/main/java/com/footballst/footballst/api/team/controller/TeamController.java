package com.footballst.footballst.api.team.controller;
import com.footballst.footballst.api.team.dto.TeamResponseDto;
import com.footballst.footballst.api.team.service.TeamService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/teams")
public class TeamController {

    private final TeamService teamService;

    @GetMapping
    public ResponseEntity<List<TeamResponseDto>> getTeams() {
        return ResponseEntity.ok(teamService.getAllTeams());
    }
}
