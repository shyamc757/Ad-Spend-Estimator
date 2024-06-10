#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
from abc import ABC, abstractmethod

class AdvertisementPlatform(ABC):
    def __init__(self, rate_card: pd.DataFrame):
        self.rate_card = rate_card

    @abstractmethod
    def calculate_expenditure(self, ad_data: pd.Series) -> float:
        pass


# In[19]:


class Instagram(AdvertisementPlatform):
    def calculate_expenditure(self, ad_data: pd.Series) -> float:
        ad_type = ad_data['type']
        if ad_type == 'image':
            return self.calculate_image_ad(ad_data)
        elif ad_type == 'video':
            return self.calculate_video_ad(ad_data)
        else:
            raise ValueError(f"Unsupported ad type: {ad_type}")

    def calculate_image_ad(self, row: pd.Series) -> float:
        impressions = row.get('impressions', 0)
        cpm = self.rate_card.loc[(self.rate_card['platform'] == 'Instagram') & (self.rate_card['ad_type'] == 'image'), 'cpm'].values[0]
        return impressions * cpm / 1000

    def calculate_video_ad(self, row: pd.Series) -> float:
        impressions = row.get('impressions', 0)
        cpm = self.rate_card.loc[(self.rate_card['platform'] == 'Instagram') & (self.rate_card['ad_type'] == 'video'), 'cpm'].values[0]
        return impressions * cpm / 1000

class Facebook(AdvertisementPlatform):
    def calculate_expenditure(self, ad_data: pd.Series) -> float:
        ad_type = ad_data['type']
        if ad_type == 'image':
            return self.calculate_image_ad(ad_data)
        elif ad_type == 'video':
            return self.calculate_video_ad(ad_data)
        else:
            raise ValueError(f"Unsupported ad type: {ad_type}")

    def calculate_image_ad(self, row: pd.Series) -> float:
        impressions = row.get('impressions', 0)
        cpm = self.rate_card.loc[(self.rate_card['platform'] == 'Facebook') & (self.rate_card['ad_type'] == 'image'), 'cpm'].values[0]
        return impressions * cpm / 1000

    def calculate_video_ad(self, row: pd.Series) -> float:
        impressions = row.get('impressions', 0)
        cpm = self.rate_card.loc[(self.rate_card['platform'] == 'Facebook') & (self.rate_card['ad_type'] == 'video'), 'cpm'].values[0]
        return impressions * cpm / 1000

class LinkedIn(AdvertisementPlatform):
    def calculate_expenditure(self, ad_data: pd.Series) -> float:
        ad_type = ad_data['type']
        if ad_type == 'image':
            return self.calculate_image_ad(ad_data)
        elif ad_type == 'text':
            return self.calculate_text_ad(ad_data)
        else:
            raise ValueError(f"Unsupported ad type: {ad_type}")

    def calculate_image_ad(self, row: pd.Series) -> float:
        impressions = row.get('impressions', 0)
        cpm = self.rate_card.loc[(self.rate_card['platform'] == 'LinkedIn') & (self.rate_card['ad_type'] == 'image'), 'cpm'].values[0]
        return impressions * cpm / 1000

    def calculate_text_ad(self, row: pd.Series) -> float:
        impressions = row.get('impressions', 0)
        cpm = self.rate_card.loc[(self.rate_card['platform'] == 'LinkedIn') & (self.rate_card['ad_type'] == 'text'), 'cpm'].values[0]
        return impressions * cpm / 1000


# In[20]:


class AdvertisementPlatformFactory:
    @staticmethod
    def get_platform(platform_name: str, rate_card: pd.DataFrame):
        if platform_name == 'Instagram':
            return Instagram(rate_card)
        elif platform_name == 'Facebook':
            return Facebook(rate_card)
        elif platform_name == 'LinkedIn':
            return LinkedIn(rate_card)
        # Add other platforms as needed
        else:
            raise ValueError(f"Unsupported platform: {platform_name}")


# In[21]:


class AdvertisementAPI:
    def __init__(self, rate_card: pd.DataFrame):
        self.rate_card = rate_card
        self.platforms = {
            'Instagram': Instagram(rate_card),
            'Facebook': Facebook(rate_card),
            'LinkedIn': LinkedIn(rate_card)
            # Add other platforms as needed
        }

    def calculate_expenditure(self, ad_data: pd.DataFrame) -> pd.DataFrame:
        expenditures = []
        for _, row in ad_data.iterrows():
            platform_name = row['platform']
            if platform_name in self.platforms:
                expenditure = self.platforms[platform_name].calculate_expenditure(row)
                expenditures.append(expenditure)
            else:
                raise ValueError(f"Unsupported platform: {platform_name}")
        
        ad_data['expenditure'] = expenditures
        return ad_data


# In[26]:


# Create rate card as a dataframe
rate_card = pd.DataFrame({
    'platform': ['Instagram', 'Instagram', 'Facebook', 'Facebook', 'LinkedIn', 'LinkedIn'],
    'ad_type': ['image', 'video', 'image', 'video', 'image', 'text'],
    'cpm': [5, 10, 4, 8, 6, 2]
})

api = AdvertisementAPI(rate_card)

# Create ad data as a dataframe
ad_data = pd.DataFrame({
    'platform': ['Instagram', 'Instagram', 'Facebook', 'LinkedIn', 'LinkedIn'],
    'type': ['image', 'video', 'image', 'text', 'image'],
    'impressions': [10000, 20000, 12500, 500000, 91000]
})

try:
    result = api.calculate_expenditure(ad_data)
    print(result)
except ValueError as e:
    print(e)


# In[ ]:




