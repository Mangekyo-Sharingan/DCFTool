import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

interface FinancialData {
  enterpriseValue: string;
  debt: string;
  cash: string;
  sharesOutstanding: string;
  lastFCF: string;
  growthRate: string;
  wacc: string;
  terminalGrowth: string;
}

export const FinancialInputs: React.FC = () => {
  const [financialData, setFinancialData] = useState<FinancialData>({
    enterpriseValue: '0',
    debt: '0',
    cash: '0',
    sharesOutstanding: '0',
    lastFCF: '0',
    growthRate: '5', // Default value as requested
    wacc: '8', // Default value as requested
    terminalGrowth: '2' // Default value as requested
  });

  useEffect(() => {
    // Listen for company data updates from the main page
    const handleDataUpdate = (event: CustomEvent) => {
      const data = event.detail;
      setFinancialData(prev => ({
        ...prev,
        enterpriseValue: data.enterprise_value?.toFixed(1) || prev.enterpriseValue,
        debt: data.debt?.toFixed(1) || prev.debt,
        cash: data.cash?.toFixed(1) || prev.cash,
        sharesOutstanding: data.shares_outstanding?.toFixed(1) || prev.sharesOutstanding,
        lastFCF: data.last_fcf?.toFixed(1) || prev.lastFCF,
        growthRate: data.growth_rate ? (data.growth_rate * 100).toFixed(1) : prev.growthRate
      }));
    };

    window.addEventListener('companyDataFetched', handleDataUpdate as EventListener);

    return () => {
      window.removeEventListener('companyDataFetched', handleDataUpdate as EventListener);
    };
  }, []);

  const handleInputChange = (field: keyof FinancialData, value: string) => {
    setFinancialData(prev => ({
      ...prev,
      [field]: value
    }));

    // Update the corresponding hidden input in the main page for form submission
    const element = document.getElementById(field.replace(/([A-Z])/g, '-$1').toLowerCase()) as HTMLInputElement;
    if (element) {
      element.value = value;
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <svg className="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
          </svg>
          <span>Financial Inputs</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="basic" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="basic">Basic</TabsTrigger>
            <TabsTrigger value="advanced">Advanced</TabsTrigger>
          </TabsList>

          <TabsContent value="basic" className="space-y-4 mt-4">
            <div className="space-y-2">
              <Label htmlFor="enterprise-value-input">Enterprise Value ($M)</Label>
              <Input
                id="enterprise-value-input"
                type="number"
                placeholder="0"
                value={financialData.enterpriseValue}
                onChange={(e) => handleInputChange('enterpriseValue', e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="debt-input">Total Debt ($M)</Label>
              <Input
                id="debt-input"
                type="number"
                placeholder="0"
                value={financialData.debt}
                onChange={(e) => handleInputChange('debt', e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="cash-input">Cash & Equivalents ($M)</Label>
              <Input
                id="cash-input"
                type="number"
                placeholder="0"
                value={financialData.cash}
                onChange={(e) => handleInputChange('cash', e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="shares-outstanding-input">Shares Outstanding (M)</Label>
              <Input
                id="shares-outstanding-input"
                type="number"
                placeholder="0"
                value={financialData.sharesOutstanding}
                onChange={(e) => handleInputChange('sharesOutstanding', e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="last-fcf-input">Last FCF ($M)</Label>
              <Input
                id="last-fcf-input"
                type="number"
                placeholder="0"
                value={financialData.lastFCF}
                onChange={(e) => handleInputChange('lastFCF', e.target.value)}
              />
            </div>
          </TabsContent>

          <TabsContent value="advanced" className="space-y-4 mt-4">
            <div className="space-y-2">
              <Label htmlFor="growth-rate-input">Growth Rate (%)</Label>
              <Input
                id="growth-rate-input"
                type="number"
                placeholder="5"
                value={financialData.growthRate}
                onChange={(e) => handleInputChange('growthRate', e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="wacc-input">WACC (%)</Label>
              <Input
                id="wacc-input"
                type="number"
                placeholder="8"
                value={financialData.wacc}
                onChange={(e) => handleInputChange('wacc', e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="terminal-growth-input">Terminal Growth Rate (%)</Label>
              <Input
                id="terminal-growth-input"
                type="number"
                placeholder="2"
                value={financialData.terminalGrowth}
                onChange={(e) => handleInputChange('terminalGrowth', e.target.value)}
              />
            </div>
          </TabsContent>
        </Tabs>

        {/* Hidden inputs for form submission - these sync with the React state */}
        <div style={{ display: 'none' }}>
          <input id="enterprise-value" value={financialData.enterpriseValue} readOnly />
          <input id="debt" value={financialData.debt} readOnly />
          <input id="cash" value={financialData.cash} readOnly />
          <input id="shares-outstanding" value={financialData.sharesOutstanding} readOnly />
          <input id="last-fcf" value={financialData.lastFCF} readOnly />
          <input id="growth-rate" value={financialData.growthRate} readOnly />
          <input id="wacc" value={financialData.wacc} readOnly />
          <input id="terminal-growth" value={financialData.terminalGrowth} readOnly />
        </div>
      </CardContent>
    </Card>
  );
};
