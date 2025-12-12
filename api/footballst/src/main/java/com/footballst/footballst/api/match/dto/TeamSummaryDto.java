package com.footballst.footballst.api.match.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class TeamSummaryDto {
    private Long teamId;
    private String name;
    private String logo;
}

