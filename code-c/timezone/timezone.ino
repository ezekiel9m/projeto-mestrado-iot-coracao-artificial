
#include <Timezone.h>   

//TimeChangeRule myDST = {"EDT", Second, Sun, Mar, 2, -240};    
TimeChangeRule mySTD = {"EST", First, Sun, Nov, 2, -300};    
Timezone myTZ(mySTD);


TimeChangeRule *tcr;      

void setup()
{
    Serial.begin(115200);
    setTime(myTZ.toUTC(compileTime()));
}

void loop()
{
    time_t utc = now();
    time_t local = myTZ.toLocal(utc, &tcr);
    Serial.println();
    //printDateTime(utc, "UTC");
    printDateTime(local, tcr -> abbrev);
    delay(10000);
}

time_t compileTime()
{
    const time_t FUDGE(10);     
    const char *compDate = __DATE__, *compTime = __TIME__, *months = "JanFebMarAprMayJunJulAugSepOctNovDec";
    char chMon[4], *m;
    tmElements_t tm;

    strncpy(chMon, compDate, 3);
    chMon[3] = '\0';
    m = strstr(months, chMon);
    tm.Month = ((m - months) / 3 + 1);

    tm.Day = atoi(compDate + 4);
    tm.Year = atoi(compDate + 7) - 1970;
    tm.Hour = atoi(compTime);
    tm.Minute = atoi(compTime + 3);
    tm.Second = atoi(compTime + 6);
    time_t t = makeTime(tm);
    return t + FUDGE;           
}


void printDateTime(time_t t, const char *tz)
{
    char currentDate[32];
    //char m[4];    
    //strcpy(m, monthShortStr(month(t)));
    sprintf(currentDate, "%.2d/%d/%d %.2d:%.2d:%.2d",
        day(t), month(t), year(t), hour(t), minute(t), second(t));
    Serial.println(currentDate);
}

