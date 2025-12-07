package com.footballst.footballst.api.player.service;
import com.footballst.footballst.api.player.PlayerRepository;
import com.footballst.footballst.api.player.dto.PlayerResponseDto;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@RequiredArgsConstructor
@Service
public class PlayerServiceImpl implements PlayerService {

    private final PlayerRepository playerRepository;

    @Override
    public List<PlayerResponseDto> getAllPlayers() {
        return playerRepository.findAll()
                .stream()
                .map(PlayerResponseDto::fromEntity)
                .toList();
    }
}

