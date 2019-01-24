package com.cl.footdata.getdata;

import java.io.Serializable;

public class DataEntity implements Serializable{
    private String vsDate;
    private String vsNum;
    private int leagId;
    private String leagName;
    private int hTeamId;
    private String hTeamName;
    private int gTeamId;
    private String gTeamName;
    private Float odds1;
    private Float odds2;
    private Float odds3;
    private int htGoal;
    private int gtGoal;
    private String result;

    public DataEntity() {
    }

    public DataEntity(String vsDate, String vsNum, String leagName, int leagId, int hTeamId, String hTeamName, int gTeamId, String gTeamName, Float odds1,
                      Float odds2, Float odds3, int htGoal, int gtGoal, String result) {
        this.vsDate = vsDate;
        this.vsNum = vsNum;
        this.leagName = leagName;
        this.leagId = leagId;
        this.hTeamId = hTeamId;
        this.hTeamName = hTeamName;
        this.gTeamId = gTeamId;
        this.gTeamName = gTeamName;
        this.odds1 = odds1;
        this.odds2 = odds2;
        this.odds3 = odds3;
        this.htGoal = htGoal;
        this.gtGoal = gtGoal;
        this.result = result;
    }

    @Override
    public String toString() {
        return "DataEntity [vsDate=" + vsDate + ", vsNum=" + vsNum + ", leagName=" + leagName + ", leagId=" + leagId + ", hTeamId=" + hTeamId + ", hTeamName="
                + hTeamName + ", gTeamId=" + gTeamId + ", gTeamName=" + gTeamName + ", odds1=" + odds1 + ", odds2=" + odds2 + ", odds3=" + odds3 + ", htGoal="
                + htGoal + ", gtGoal=" + gtGoal + ", result=" + result + "]";
    }

    public String getVsDate() {
        return vsDate;
    }

    public void setVsDate(String vsDate) {
        this.vsDate = vsDate;
    }

    public String getVsNum() {
        return vsNum;
    }

    public void setVsNum(String vsNum) {
        this.vsNum = vsNum;
    }

    public String getLeagName() {
        return leagName;
    }

    public void setLeagName(String leagName) {
        this.leagName = leagName;
    }

    public int getLeagId() {
        return leagId;
    }

    public void setLeagId(int leagId) {
        this.leagId = leagId;
    }

    public int gethTeamId() {
        return hTeamId;
    }

    public void sethTeamId(int hTeamId) {
        this.hTeamId = hTeamId;
    }

    public String gethTeamName() {
        return hTeamName;
    }

    public void sethTeamName(String hTeamName) {
        this.hTeamName = hTeamName;
    }

    public int getgTeamId() {
        return gTeamId;
    }

    public void setgTeamId(int gTeamId) {
        this.gTeamId = gTeamId;
    }

    public String getgTeamName() {
        return gTeamName;
    }

    public void setgTeamName(String gTeamName) {
        this.gTeamName = gTeamName;
    }

    public Float getOdds1() {
        return odds1;
    }

    public void setOdds1(Float odds1) {
        this.odds1 = odds1;
    }

    public Float getOdds2() {
        return odds2;
    }

    public void setOdds2(Float odds2) {
        this.odds2 = odds2;
    }

    public Float getOdds3() {
        return odds3;
    }

    public void setOdds3(Float odds3) {
        this.odds3 = odds3;
    }

    public int getHtGoal() {
        return htGoal;
    }

    public void setHtGoal(int htGoal) {
        this.htGoal = htGoal;
    }

    public int getGtGoal() {
        return gtGoal;
    }

    public void setGtGoal(int gtGoal) {
        this.gtGoal = gtGoal;
    }

    public String getResult() {
        return result;
    }

    public void setResult() {
        if(this.htGoal>this.gtGoal){
            this.result="胜";
        } else if(this.htGoal<this.gtGoal){
            this.result="负";
        } else{
            this.result="平";
        }
    }

}
