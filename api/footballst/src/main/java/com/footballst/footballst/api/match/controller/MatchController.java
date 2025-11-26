package com.footballst.footballst.api.match.controller;

import com.footballst.footballst.api.match.Match;
import com.footballst.footballst.api.match.service.MatchService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/matches")
public class MatchController {
    private final MatchService matchService;

    @GetMapping
    public ResponseEntity<List<Match>> getMatches() {
        return ResponseEntity.ok(matchService.getAllMatches());
    }
}

