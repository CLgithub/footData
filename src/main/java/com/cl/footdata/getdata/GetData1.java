package com.cl.footdata.getdata;

/**
 * 近几年足球比赛得分数据采集，数据来源http://www.sporttery.cn，
 * http://info.sporttery.cn/football/match_result.php?page=2&search_league=0&start_date=2019-01-22&end_date=2019-01-24&dan=0
 * 除采集比分外，还采集赔率信息
 */

import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import org.apache.commons.beanutils.BeanUtils;
import org.apache.commons.dbutils.DbUtils;
import org.apache.http.Consts;
import org.apache.http.HttpEntity;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;
import org.apache.log4j.Logger;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;
import com.cl.common.utils.JDBCUtilHikariCP;

public class GetData1 {
    public static void main(String[] args) throws ClientProtocolException, IOException, SQLException {
        service();
    }

    static Logger logger=Logger.getLogger(GetData1.class);

    public static void service() {
        SimpleDateFormat sdf1=new SimpleDateFormat("yyyy-MM-dd");
        Calendar calendar=Calendar.getInstance();
        calendar.set(Calendar.DATE, calendar.get(Calendar.DATE) - 2);
        String endDate = sdf1.format(calendar.getTime());	//当前前2天
        Connection conn=null;
        CloseableHttpClient cHttpClient_http=null;
        CloseableHttpResponse response=null;
        try {
            conn=JDBCUtilHikariCP.getConnection();
			conn.setAutoCommit(false);
            cHttpClient_http=HttpClients.createDefault();
            String beginDate=getBeginDate(conn); //查询数据获取最后日前+1

            String url="http://info.sporttery.cn/football/match_result.php";
//			String beginDate="2019-01-01";
//			endDate="2019-01-07";
            Map<String, String> paramDatas= new HashMap<String, String>();
            paramDatas.put("search_league","0");
            paramDatas.put("start_date",beginDate);
            paramDatas.put("end_date",endDate);
            paramDatas.put("dan","");
            int tPage=1;

            logger.info("准备查询"+beginDate+"～"+endDate+"的数据");
            for(int i=1;i<=tPage;i++){
                logger.info("开始解析第"+i+"页");
                paramDatas.put("page",i+"");
                response= exeRequest(cHttpClient_http, url, paramDatas, null);
                String content = EntityUtils.toString(response.getEntity(),"gbk");
                int i1 = content.indexOf("<!--表格开始-->");
                int i2 = content.indexOf("<!--表格结束-->");
                String html=content.substring(i1, i2);
                List<DataEntity> list= resHtml(html);
                list=setId(list,conn);
                tPage=getTPage(html);
                logger.info("第"+i+"页解析到"+list.size()+"条数据");
                saveData(list,conn);
//				for(DataEntity dataEntity:list){
//					System.out.println(dataEntity);
//				}
            }
            conn.commit();
        } catch (Exception e) {
            logger.error("执行有误：",e);
        } finally {
            try {
                DbUtils.close(conn);
            } catch (SQLException e) {
                e.printStackTrace();
            } finally {
                try {
                    if(cHttpClient_http!=null) cHttpClient_http.close();
                } catch (IOException e) {
                    e.printStackTrace();
                } finally {
                    try {
                        if(response!=null) response.close();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
    }

    /**
     * 设置ID 当有新的联赛或球队入库时，需要为其设置ID
     * @param list 数据
     * @param conn 数据库连接
     * @return
     */
    private static List<DataEntity> setId(List<DataEntity> list, Connection conn) {
        List<DataEntity> list2=new ArrayList<DataEntity>();
        String sql1="select id from t_football_data_dict where name=?";
        String sql2="insert into t_football_data_dict(id,type,name) select max(id)+1,1,? from t_football_data_dict";
        String sql3="insert into t_football_data_dict(id,type,name) select max(id)+1,2,? from t_football_data_dict";
        PreparedStatement ps1=null;
        PreparedStatement ps2=null;
        PreparedStatement ps3=null;
        ResultSet rs1=null;
        try {
            ps1=conn.prepareStatement(sql1);
            ps2=conn.prepareStatement(sql2);
            ps3=conn.prepareStatement(sql3);
            for(DataEntity dataEntity:list){
                DataEntity dataEntity2 = new DataEntity();
                ps1.setString(1, dataEntity.getLeagName());
                rs1=ps1.executeQuery();
                int id=0;
                if(rs1.next()){
                    id=rs1.getInt(1);
                    dataEntity.setLeagId(id);
                }else{
                    logger.info("有未知联赛");
                    ps2.setString(1, dataEntity.getLeagName());
                    ps2.executeUpdate();
                }

                ps1.setString(1, dataEntity.getgTeamName());
                rs1=ps1.executeQuery();
                id=0;
                if(rs1.next()){
                    id=rs1.getInt(1);
                    dataEntity.setgTeamId(id);
                }else{
                    logger.info("有未知客队");
                    ps3.setString(1, dataEntity.getgTeamName());
                    ps3.executeUpdate();
                }

                ps1.setString(1, dataEntity.gethTeamName());
                rs1=ps1.executeQuery();
                id=0;
                if(rs1.next()){
                    id=rs1.getInt(1);
                    dataEntity.sethTeamId(id);
                }else{
                    logger.info("有未知主队");
                    ps3.setString(1, dataEntity.gethTeamName());
                    ps3.executeUpdate();
                }
                BeanUtils.copyProperties(dataEntity2, dataEntity);
                dataEntity2.setResult();
                list2.add(dataEntity2);
            }
            return list2;
        } catch (Exception e) {
            logger.error("设置id有误：",e);
        } finally {
            try {
                if(ps1!=null)ps1.close();
            } catch (SQLException e) {
                e.printStackTrace();
            } finally {
                try {
                    if(ps2!=null)ps2.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }finally {
                    try {
                        if(rs1!=null)rs1.close();
                    } catch (SQLException e) {
                        e.printStackTrace();
                    } finally {
                        try {
                            if(ps3!=null)ps3.close();
                        } catch (SQLException e) {
                            e.printStackTrace();
                        }
                    }
                }
            }
        }
        return null;
    }

    /**
     * 获取数据中最大日前后一天日期
     * @param conn
     * @return
     */
    private static String getBeginDate(Connection conn) {
        String sql="select to_char(max(vsdate)+1,'yyyy-MM-dd') from t_football_data_1";
        PreparedStatement ps1=null;
        ResultSet rs1=null;
        try {
            ps1 = conn.prepareStatement(sql);
            rs1 = ps1.executeQuery();
            if(rs1.next()){
                String string = rs1.getString(1);
                return string;
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            try {
                if(ps1!=null)ps1.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
        return null;
    }

    /**
     * 存储数据
     * @param list
     * @param connection
     */
    private static void saveData(List<DataEntity> list, Connection connection) {
        logger.info("开始存储数据");
        String sql="insert into t_football_data_1(vsDate, vsNum, leagName, hTeamName, gTeamName, odds1, odds2, odds3, htGoal, gtGoal, result, leagId, hTeamId, gTeamId ) "
                + " values(to_date(?,'yyyy-MM-dd'),?,?,?,?,?,?,?,?,?,?,?,?,?)";
        PreparedStatement ps1=null;
        try {
            ps1= connection.prepareStatement(sql);
            for(DataEntity dataEntity:list){
                ps1.setString(1,dataEntity.getVsDate());
                ps1.setString(2,dataEntity.getVsNum());
                ps1.setString(3, dataEntity.getLeagName());
                ps1.setString(4, dataEntity.gethTeamName());
                ps1.setString(5, dataEntity.getgTeamName());
                ps1.setFloat(6, dataEntity.getOdds1());
                ps1.setFloat(7, dataEntity.getOdds2());
                ps1.setFloat(8, dataEntity.getOdds3());
                ps1.setInt(9, dataEntity.getHtGoal());
                ps1.setInt(10, dataEntity.getGtGoal());
                ps1.setString(11, dataEntity.getResult());
                ps1.setInt(12, dataEntity.getLeagId());
                ps1.setInt(13, dataEntity.gethTeamId());
                ps1.setInt(14, dataEntity.getgTeamId());
                ps1.addBatch();
            }
            ps1.executeBatch();
            logger.info("插入完成:"+list.size());
        } catch (Exception e) {
            logger.error("存储数据有误", e);
        }finally {
            try {
                if(ps1!=null)ps1.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * 获取有多少页
     * @date 2019年1月8日
     * @param html
     * @return
     */
    private static int getTPage(String html) {
        Document document = Jsoup.parse(html);
        Elements table_es = document.getElementsByTag("table");
        try {
            String size= table_es.get(1).getElementsByTag("span").get(1).text();
            int tPage=Integer.parseInt(size)/30+1;
            return tPage;
        } catch (RuntimeException e) {
            logger.info("数据为空");
            return 0;
        }

    }

    /**
     * 解析html,封装成list数据
     * @param html
     * @return
     */
    private static List<DataEntity> resHtml(String html) {
        List<DataEntity> list=new ArrayList<DataEntity>();
        Document document = Jsoup.parse(html);
        Elements table_es = document.getElementsByTag("table");
        Elements tr_es= table_es.get(0).getElementsByTag("tr");
        for(int i=0;i<tr_es.size()-2;i++){
            Elements td_es= tr_es.get(i).getElementsByTag("td");
//    		if(!"--".equals(td_es.get(6).text())&&!"取消".equals(td_es.get(5).text())){
            if(!"取消".equals(td_es.get(5).text())&&"已完成".equals(td_es.get(9).text())){
                DataEntity dataEntity = new DataEntity();
                for(int j=0;j<td_es.size();j++){
                    dataEntity.setVsDate(td_es.get(0).text());
                    dataEntity.setVsNum(td_es.get(1).text());
                    dataEntity.setLeagName(td_es.get(2).attr("title"));
                    Elements span_es = td_es.get(3).getElementsByTag("span");
                    dataEntity.sethTeamName(span_es.get(0).attr("title")
                            .replace(" ", "").replace("顿", "敦").replace("莫","摩")
                            .replace("吕","鲁").replace("贝","伯").replace("队",""));
                    dataEntity.setgTeamName(span_es.get(2).attr("title").
                            replace(" ", "").replace("顿", "敦").replace("莫","摩")
                            .replace("吕","鲁").replace("贝","伯").replace("队",""));
                    dataEntity.setOdds1(Float.parseFloat("--".equals(td_es.get(6).text())?"0":td_es.get(6).text()));
                    dataEntity.setOdds2(Float.parseFloat("--".equals(td_es.get(7).text())?"0":td_es.get(7).text()));
                    dataEntity.setOdds3(Float.parseFloat("--".equals(td_es.get(8).text())?"0":td_es.get(8).text()));
                    dataEntity.setHtGoal(Integer.parseInt(td_es.get(5).text().split(":", -1)[0]));
                    dataEntity.setGtGoal(Integer.parseInt(td_es.get(5).text().split(":", -1)[1]));
                }
                dataEntity.setResult();
                list.add(dataEntity);
            }
        }
        return list;
    }


    /**
     * 执行请求，不管是http请求还是https请求都是这个模式，有所不同的是httpClient不同，https的客户端要用上面方法获取
     * @author chenlei
     * @date 2018年9月28日
     * @param cHttpClient http或https客户端
     * @param url 请求地址
     * @param paramDatas 请求参数键值对列表
     * @param jsession jsessionid
     * @return CloseableHttpResponse
     * @throws ClientProtocolException
     * @throws IOException
     */
    public static CloseableHttpResponse exeRequest(CloseableHttpClient cHttpClient, String url, Map<String, String> paramDatas, String jsession) throws ClientProtocolException, IOException{
        HttpPost httpPost=new HttpPost(url);
        // 设置请求参数
        List<NameValuePair> nvps = new ArrayList<NameValuePair>();
        if(paramDatas!=null){
            Set<Entry<String,String>> entrySet = paramDatas.entrySet();
            for(Iterator<Entry<String, String>> iterator = entrySet.iterator();iterator.hasNext();){
                Entry<String, String> entry = iterator.next();
                nvps.add(new BasicNameValuePair(entry.getKey(), entry.getValue()));
            }
        }
        HttpEntity reqEntity = new UrlEncodedFormEntity(nvps, Consts.UTF_8);
        httpPost.setEntity(reqEntity);
        if(jsession!=null){
            httpPost.setHeader("Cookie", "JSESSIONID=" + jsession);
        }

        CloseableHttpResponse closeableHttpResponse = cHttpClient.execute(httpPost);
//		closeableHttpResponse.close();
//		cHttpClient.close();
        return closeableHttpResponse;
    }

}
