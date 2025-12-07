package com.footballst.footballst.api.matchDetail.controller;

import com.footballst.footballst.api.matchDetail.dto.MatchDetailResponseDto;
import com.footballst.footballst.api.matchDetail.service.MatchDetailService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/matches")
public class MatchDetailController {

    private final MatchDetailService matchDetailService;

    @GetMapping("/{matchId}/detail")
    public MatchDetailResponseDto getDetail(@PathVariable Long matchId) {
        return matchDetailService.getMatchDetail(matchId);
    }
}



