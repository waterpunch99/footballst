package com.footballst.footballst.api.player.controller;
import com.footballst.footballst.api.player.dto.PlayerResponseDto;
import com.footballst.footballst.api.player.service.PlayerService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/players")
public class PlayerController {

    private final PlayerService playerService;

    @GetMapping
    public ResponseEntity<List<PlayerResponseDto>> getPlayers() {
        return ResponseEntity.ok(playerService.getAllPlayers());
    }
}

