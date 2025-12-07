package com.footballst.footballst.api.player.service;
import com.footballst.footballst.api.player.dto.PlayerResponseDto;

import java.util.List;

public interface PlayerService {
    List<PlayerResponseDto> getAllPlayers();
}
