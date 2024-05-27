class CSVHandler
{
public:
    static CSVHandler &getInstance()
    {
        static CSVHandler instance;
        return instance;
    }


private:
    CSVHandler() {}
    ~CSVHandler() {}
    CSVHandler(const CSVHandler &) = delete;
    CSVHandler   &operator=(const CSVHandler &) = delete;
};