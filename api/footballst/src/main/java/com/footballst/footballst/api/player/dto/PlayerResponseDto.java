package com.footballst.footballst.api.player.dto;
import com.footballst.footballst.api.player.Player;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class PlayerResponseDto {

    private String playerId;
    private String name;
    private String age;
    private String number;
    private String position;
    private String photo;

    public static PlayerResponseDto fromEntity(Player p) {
        return PlayerResponseDto.builder()
                .playerId(p.getId())
                .name(p.getName())
                .age(p.getAge())
                .number(p.getNumber())
                .position(p.getPosition())
                .photo(p.getPhoto())
                .build();
    }
}
